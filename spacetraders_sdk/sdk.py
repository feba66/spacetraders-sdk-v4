from datetime import datetime, timezone
import os
import time
import logging

from spacetraders_sdk.path_finder import Options, PathFinder, Priority
from spacetraders_sdk.util import system_symbol_from_wp

from .logger import Logger
from .storage import RedisStorage, Storage
from .astar import dist, AStarNode, CostNode, AStarSearch
from .openapi_client import (
    Agent,
    AgentsApi,
    ApiClient,
    ApiException,
    Configuration,
    Contract,
    ContractsApi,
    DefaultApi,
    DeliverContractRequest,
    Faction,
    FactionsApi,
    FactionSymbol,
    FleetApi,
    Market,
    NavigateShipRequest,
    PurchaseCargoRequest,
    PurchaseShipRequest,
    RefuelShipRequest,
    RegisterRequest,
    Ship,
    ShipNavStatus,
    ShipType,
    Shipyard,
    System,
    SystemsApi,
    TradeSymbol,
    Waypoint,
)
from pprint import pprint
import redis


class API:
    config: Configuration
    client: ApiClient
    agents_api: AgentsApi
    fleet_api: FleetApi
    default_api: DefaultApi
    systems_api: SystemsApi
    contracts_api: ContractsApi
    factions_api: FactionsApi


class SDK:
    api: API
    logger: logging.Logger
    storage: Storage
    pathfinder: PathFinder

    agent: Agent
    contracts: dict[str, Contract]
    faction: Faction
    token: str
    ships: dict[str, Ship]
    systems: dict[str, System]
    waypoints: dict[str, Waypoint]
    shipyards: dict[str, Shipyard]
    markets: dict[str, Market]
    red: redis.Redis
    REDIS_PREFIX = "st"
    username: str

    def __init__(self, token: str | None = None, host: str | None = None, username: str | None = None):
        self.api = API()
        self.systems = {}
        self.ships = {}
        self.contracts = {}
        self.waypoints = {}
        self.shipyards = {}
        self.markets = {}
        self.username = username
        self.red = redis.Redis(host="localhost", port=6379, db=0)

        self.logger = Logger("SDKv4")
        self.storage = RedisStorage("localhost")
        self.pathfinder = PathFinder(self.storage)

        self.api.config = Configuration(host="https://api.spacetraders.io/v2" if host is None else host)
        if token is not None:
            self.api.config.access_token = token

        self.api.client = ApiClient(self.api.config)

        self.api.agents_api = AgentsApi(self.api.client)
        self.api.fleet_api = FleetApi(self.api.client)
        self.api.default_api = DefaultApi(self.api.client)
        self.api.systems_api = SystemsApi(self.api.client)
        self.api.contracts_api = ContractsApi(self.api.client)
        self.api.factions_api = FactionsApi(self.api.client)

    def register(self, username: str, faction: FactionSymbol | str = FactionSymbol.ASTRO):  # noqa
        if isinstance(faction, str):
            faction = FactionSymbol(faction)
        r = self.api.default_api.register(RegisterRequest(symbol=username, faction=faction))

        self._set_agent(r.data.agent)
        self.contracts = {r.data.contract.id: r.data.contract}
        self.faction = r.data.faction
        self._set_ship(r.data.ship)
        self.token = r.data.token
        self.logger.info(f"Registered as {self.agent.symbol} with token {r.data.token}")
        return r.data

    def get_agent(self, force=False):  # RedisStorage
        if not force:
            agent = self.storage.get_agent()
            if agent:
                return agent
        r = self.api.agents_api.get_my_agent()
        self.storage.set_agent(r.data)
        return r.data

    def get_contracts(self):
        page, total = 0, 1
        while page <= total:
            page += 1
            r = self.api.contracts_api.get_contracts(page=page, limit=20)
            total = r.meta.total / 20
            for c in r.data:
                self._set_contract(c)
        return r.data

    def accept_contract(self, contract: Contract | str):
        if isinstance(contract, str):
            contract = self.contracts[contract]
        r = self.api.contracts_api.accept_contract(contract.id)
        self._set_agent(r.data.agent)
        self._set_contract(r.data.contract)
        self.logger.info(f"Accepted contract {contract.id}")
        return r.data.contract

    def deliver_contract(
        self,
        ship: Ship | str,
        contract: Contract | str,
        trade_symbol: TradeSymbol | str,
        units: int,
    ):
        if isinstance(ship, str):
            ship = self.storage.get_ship(ship)
        if isinstance(contract, str):
            contract = self.contracts[contract]
        if isinstance(trade_symbol, TradeSymbol):
            trade_symbol = trade_symbol.value

        self.check_nav_status(ship, ShipNavStatus.DOCKED)

        r = self.api.contracts_api.deliver_contract(
            contract.id,
            DeliverContractRequest(shipSymbol=ship.symbol, tradeSymbol=trade_symbol, units=units),
        )
        self._set_contract(r.data.contract)
        # self.ships[ship.symbol].cargo = r.data.cargo
        self.storage.set_ship_cargo(ship, r.data.cargo)
        # self._set_ship(self.ships[ship.symbol])
        self.logger.info(f"Delivered contract {contract.id} {units}x {trade_symbol}")
        return r.data.contract

    def fulfill_contract(self, contract: Contract | str):
        if isinstance(contract, str):
            contract = self.contracts[contract]
        r = self.api.contracts_api.fulfill_contract(contract.id)
        self._set_agent(r.data.agent)
        self._set_contract(r.data.contract)
        self.logger.info(f"Fulfilled contract {contract.id}")
        return r.data.contract

    def negotiate_contract(self, ship: Ship | str):
        if isinstance(ship, str):
            ship = self.storage.get_ship(ship)
        r = self.api.fleet_api.negotiate_contract(ship.symbol)
        self._set_contract(r.data.contract)
        self.logger.info(f"Negotiated contract {r.data.contract.id}")
        return r.data.contract

    def get_ships(self, force=False):  # RedisStorage
        if not force:
            agent = self.get_agent()
            # ships = self._get_ships()
            ships = self.storage.get_ships()
            if ships and len(ships) == agent.ship_count:
                return ships

        page, total = 0, 1
        while page <= total:
            page += 1
            r = self.api.fleet_api.get_my_ships(page=page, limit=20)
            total = r.meta.total / 20
            for s in r.data:
                # self._set_ship(s)
                self.storage.set_ship(s)
        return r.data

    def get_system(self, system_symbol: str, force=False):  # RedisStorage
        if not force:
            system = self.storage.get_system(system_symbol)
            if system:
                return system

        r = self.api.systems_api.get_system(system_symbol)
        self.storage.set_system(r.data)
        return r.data

    def get_waypoints(self, system: str, force=False):  # RedisStorage
        if not force:
            waypoints = self.storage.get_waypoints()
            if waypoints:
                return [waypoint for waypoint in waypoints if waypoint.system_symbol == system]
        page, total = 0, 0
        waypoints = []
        while page <= total:
            page += 1
            r = self.api.systems_api.get_system_waypoints(system, page=page, limit=20)
            total = r.meta.total / 20
            for waypoint in r.data:
                self.storage.set_waypoint(waypoint)
                waypoints.append(waypoint)
        return waypoints

    def get_shipyard(self, system, waypoint, force=False):  # RedisStorage
        if not force:
            shipyard = self.storage.get_shipyard(waypoint)
            if shipyard:
                return shipyard
        r = self.api.systems_api.get_shipyard(system, waypoint)
        self.storage.set_shipyard(r.data)
        return r.data

    def dock(self, ship: Ship | str):  # RedisStorage
        if isinstance(ship, Ship):
            ship = ship.symbol
        r = self.api.fleet_api.dock_ship(ship)
        self.storage.set_ship_nav(ship, r.data.nav)
        return r.data

    def orbit(self, ship: Ship | str):  # RedisStorage
        if isinstance(ship, Ship):
            ship = ship.symbol
        r = self.api.fleet_api.orbit_ship(ship)
        self.storage.set_ship_nav(ship, r.data.nav)
        return r.data

    def navigate(self, ship: Ship | str, waypoint: Waypoint | str):  # RedisStorage
        if isinstance(ship, Ship):
            ship = ship.symbol
        if isinstance(waypoint, Waypoint):
            waypoint = waypoint.symbol
        nav = self.storage.get_ship_nav(ship)
        if nav.waypoint_symbol == waypoint:
            return None
        fuel = self.storage.get_ship_fuel(ship)
        ship_waypoint = self.storage.get_waypoint(nav.waypoint_symbol)
        target_waypoint = self.storage.get_waypoint(waypoint)
        if fuel.capacity < dist(ship_waypoint, target_waypoint):
            raise Exception("Not enough range")
        self.check_nav_status(ship, ShipNavStatus.IN_ORBIT)

        r = self.api.fleet_api.navigate_ship(ship, NavigateShipRequest(waypointSymbol=waypoint))
        self.storage.set_ship_nav(ship, r.data.nav)
        self.storage.set_ship_fuel(ship, r.data.fuel)
        old_wp = nav.waypoint_symbol
        self.logger.info(
            f"Ship {ship} is navigating from {old_wp} to {waypoint} t={(r.data.nav.route.arrival - r.data.nav.route.departure_time).total_seconds():.2f}s fuel={r.data.fuel.consumed.amount} d={dist(r.data.nav.route.destination, r.data.nav.route.origin):.2f}"
        )
        return r.data

    def buy_ship(self, waypoint: Waypoint | str, ship_type: ShipType | str):  # RedisStorage
        if isinstance(waypoint, Waypoint):
            waypoint = waypoint.symbol
        if isinstance(ship_type, str):
            ship_type = ShipType(ship_type)
        r = self.api.fleet_api.purchase_ship(PurchaseShipRequest(shipType=ship_type, waypointSymbol=waypoint))
        # self._set_agent(r.data.agent)
        self.storage.set_agent(r.data.agent)
        self.storage.set_ship(r.data.ship)
        # self._set_ship(r.data.ship)
        self.logger.info(f"Bought ship {r.data.ship.symbol} {r.data.transaction}")

        return r.data

    def get_market(self, system: System | str, waypoint: Waypoint | str, force=False):  # RedisStorage
        if isinstance(system, System):
            system = system.symbol
        if isinstance(waypoint, Waypoint):
            waypoint = waypoint.symbol
        if not force:
            market = self.storage.get_market(waypoint)
            if market:
                return market
        r = self.api.systems_api.get_market(system, waypoint)
        self.storage.set_market(r.data)
        return r.data

    def buy_good(self, ship: Ship | str, trade_good: TradeSymbol | str, units: int):  # RedisStorage
        if isinstance(ship, str):
            ship = self.storage.get_ship(ship)
        if isinstance(trade_good, str):
            trade_good = TradeSymbol(trade_good)

        self.check_nav_status(ship, ShipNavStatus.DOCKED)

        r = self.api.fleet_api.purchase_cargo(ship.symbol, PurchaseCargoRequest(symbol=trade_good, units=units))

        self.storage.set_agent(r.data.agent)
        self.storage.set_ship_cargo(ship, r.data.cargo)

        self.logger.info(f"Bought {units} units of {trade_good} {r.data.transaction}")
        return r.data

    def sell_good(self, ship: Ship | str, trade_good: TradeSymbol | str, units: int):  # RedisStorage
        if isinstance(ship, str):
            ship = self.storage.get_ship(ship)
        if isinstance(trade_good, str):
            trade_good = TradeSymbol(trade_good)

        self.check_nav_status(ship, ShipNavStatus.DOCKED)

        r = self.api.fleet_api.sell_cargo(ship.symbol, PurchaseCargoRequest(symbol=trade_good, units=units))

        self.storage.set_agent(r.data.agent)
        self.storage.set_ship_cargo(ship, r.data.cargo)

        self.logger.info(f"Sold {units} units of {trade_good} {r.data.transaction}")
        return r.data

    def refuel(self, ship: Ship | str, units: int | None = None, from_cargo: bool = False):  # RedisStorage
        if isinstance(ship, Ship):
            ship = ship.symbol
        self.check_nav_status(ship, ShipNavStatus.DOCKED)
        r = self.api.fleet_api.refuel_ship(ship, RefuelShipRequest(units=units, fromCargo=from_cargo))

        self.storage.set_agent(r.data.agent)
        self.storage.set_ship_fuel(ship, r.data.fuel)

        self.logger.info(f"Refueled {units} units {r.data.transaction}")
        return r.data

    #

    def check_nav_status(self, ship: Ship | str, wanted_status: ShipNavStatus | str):  # RedisStorage
        if isinstance(ship, Ship):
            ship = ship.symbol
        nav = self.storage.get_ship_nav(ship)
        if nav.status == ShipNavStatus.IN_TRANSIT:
            t = (nav.route.arrival - datetime.now(timezone.utc)).total_seconds() + 0.2
            self.logger.info(f"Ship {ship} is in transit, waiting {t:.2f}s")
            time.sleep(t)
        if nav.status != wanted_status:
            if wanted_status == ShipNavStatus.IN_ORBIT:
                self.orbit(ship)
            elif wanted_status == ShipNavStatus.DOCKED:
                self.dock(ship)
            else:
                raise Exception(f"What status did you want? You're imagining things: {wanted_status}")

    def check_cooldown(self, ship: Ship | str):  # RedisStorage
        if isinstance(ship, Ship):
            ship = ship.symbol
        cooldown = self.storage.get_ship_cooldown(ship)
        if cooldown.expiration and cooldown.expiration > datetime.now(timezone.utc):
            t = (cooldown.expiration - datetime.now(timezone.utc)).seconds
            self.logger.info(f"Ship {ship} is on cooldown, waiting {t:.2f}s")
            time.sleep(t)

    def filter_markets(self, good: TradeSymbol | str):  # RedisStorage
        if isinstance(good, str):
            good = TradeSymbol(good)

        have_good = []
        for market in self.storage.get_markets():
            for im in market.imports:
                if im.symbol == good:
                    have_good.append(("im", market))
            for ex in market.exports:
                if ex.symbol == good:
                    have_good.append(("ou", market))
            for exchange in market.exchange:
                if exchange.symbol == good:
                    have_good.append(("ex", market))
        return have_good

    def route_to(self, ship: Ship | str, goal: Waypoint | str, start: str | None = None):
        if isinstance(ship, Ship):
            ship = ship.symbol
        if isinstance(goal, Waypoint):
            goal = goal.symbol

        nav = self.storage.get_ship_nav(ship)
        ship_obj = self.storage.get_ship(ship)
        fuel = self.storage.get_ship_fuel(ship)

        options = Options(
            radius=fuel.capacity,
            flight_mode=nav.flight_mode,
            engine_speed=ship_obj.engine.speed,
            priority=Priority.TIME,
            system=nav.system_symbol,
        )
        route = self.pathfinder.get_route(nav.waypoint_symbol if not start else start, goal, options)
        return route

    def navigate_to(self, ship: Ship | str, goal: Waypoint | str):
        route = self.route_to(ship, goal)

        print(route)
        for wp in route.path[1:]:
            self.refuel(ship)
            nav = self.storage.get_ship_nav(ship)
            meta = self.storage.get_market_meta(nav.waypoint_symbol)
            if meta is None or time.time() - meta > 5 * 60:  # TODO: disable this when nearing ratelimit
                self.check_nav_status(ship, ShipNavStatus.IN_ORBIT)
                self.get_market(nav.system_symbol, nav.waypoint_symbol, True)
            self.navigate(ship, wp)

    class Helpers:
        @staticmethod
        def dist(a: Waypoint | System, b: Waypoint | System):
            return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

        @staticmethod
        def assemble_node_list(system, radius, markets: list[str] | None = None):
            node_list = []
            for wp in system.waypoints:
                if markets and wp.symbol not in markets:
                    continue
                connections = []
                for wp2 in system.waypoints:
                    if wp.symbol != wp2.symbol and dist(wp, wp2) < radius:
                        connections.append(CostNode(wp2.symbol, SDK.Helpers.dist(wp, wp2)))
                node_list.append(AStarNode(wp.symbol, connections, wp.x, wp.y))
            return node_list
