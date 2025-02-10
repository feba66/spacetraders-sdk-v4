from datetime import datetime, timezone
import os
import time
import logging

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

        self.logger = logging.getLogger("sdk")
        logging.basicConfig(filename="sdk.log", level=logging.INFO)

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

    def _set_agent(self, agent: Agent):
        self.agent = agent
        self.red.set(f"{self.REDIS_PREFIX}:{agent.symbol}:agent", agent.to_json())

    def _get_agent(self, symbol: str) -> Agent:
        jsn = self.red.get(f"{self.REDIS_PREFIX}:{symbol}:agent")
        if jsn:
            return Agent.from_json(jsn)
        return None

    def _set_ship(self, ship: Ship):
        self.ships[ship.symbol] = ship
        self.red.hset(f"{self.REDIS_PREFIX}:{self.agent.symbol}:ships", f"{ship.symbol}", ship.to_json())

    def _get_ship(self, symbol: str) -> Ship:
        jsn = self.red.hget(f"{self.REDIS_PREFIX}:{self.agent.symbol}:ships", f"{symbol}")
        if jsn:
            return Ship.from_json(jsn)
        return None

    def _get_ships(self):
        jsn = self.red.hgetall(f"{self.REDIS_PREFIX}:{self.agent.symbol}:ships")
        if jsn:
            return {k.decode(): Ship.from_json(v) for k, v in jsn.items()}
        return None

    def _set_contract(self, contract: Contract):
        self.contracts[contract.id] = contract
        self.red.hset(f"{self.REDIS_PREFIX}:{self.agent.symbol}:contracts", f"{contract.id}", contract.to_json())

    def _set_system(self, system: System):
        self.systems[system.symbol] = system
        self.red.hset(f"{self.REDIS_PREFIX}:systems", f"{system.symbol}", system.to_json())

    def _get_system(self, symbol: str) -> System:
        jsn = self.red.hget(f"{self.REDIS_PREFIX}:systems", f"{symbol}")
        if jsn:
            return System.from_json(jsn)
        return None

    def _get_waypoints(self, system: str):
        waypoints = self.red.hgetall(f"{self.REDIS_PREFIX}:waypoints:{system}")
        if waypoints:
            return {k.decode(): Waypoint.from_json(v) for k, v in waypoints.items()}
        return None

    def _get_waypoint(self, system: str, waypoint: str):
        jsn = self.red.hget(f"{self.REDIS_PREFIX}:waypoints:{system}", f"{waypoint}")
        if jsn:
            return Waypoint.from_json(jsn)
        return None

    def _set_waypoint(self, system: str, waypoint: Waypoint):
        self.waypoints[waypoint.symbol] = waypoint
        self.red.hset(f"{self.REDIS_PREFIX}:waypoints:{system}", f"{waypoint.symbol}", waypoint.to_json())

    def _set_shipyard(self, shipyard: Shipyard):
        self.shipyards[shipyard.symbol] = shipyard
        self.red.hset(f"{self.REDIS_PREFIX}:shipyards", f"{shipyard.symbol}", shipyard.to_json())

    def _get_shipyard(self, symbol: str) -> Shipyard:
        jsn = self.red.hget(f"{self.REDIS_PREFIX}:shipyards", f"{symbol}")
        if jsn:
            return Shipyard.from_json(jsn)
        return None

    def _get_shipyards(self):
        jsn = self.red.hgetall(f"{self.REDIS_PREFIX}:shipyards")
        if jsn:
            return {k.decode(): Shipyard.from_json(v) for k, v in jsn.items()}
        return None

    def _set_market(self, market: Market):
        self.markets[market.symbol] = market
        self.red.hset(f"{self.REDIS_PREFIX}:markets", f"{market.symbol}", market.to_json())

    def _get_market(self, waypoint: Waypoint):
        jsn = self.red.hget(f"{self.REDIS_PREFIX}:markets", f"{waypoint.symbol}")
        if jsn:
            return Market.from_json(jsn)
        return None

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

    def get_agent(self):
        if self.username:
            agent = self._get_agent(self.username)
            if agent:
                self.agent = agent
                return agent
        r = self.api.agents_api.get_my_agent()
        self._set_agent(r.data)
        return r.data

    def get_contracts(self):
        page, total = 1, 1
        while page <= total:
            r = self.api.contracts_api.get_contracts(page=page, limit=20)
            total = r.meta.total / 20
            for c in r.data:
                self._set_contract(c)
            page += 1
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
            ship = self.ships[ship]
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
        self.ships[ship.symbol].cargo = r.data.cargo
        self._set_ship(self.ships[ship.symbol])
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
            ship = self.ships[ship]
        r = self.api.fleet_api.negotiate_contract(ship.symbol)
        self._set_contract(r.data.contract)
        self.logger.info(f"Negotiated contract {r.data.contract.id}")
        return r.data.contract

    def get_ships(self, force=False):
        if not force:
            if not self.agent:
                self.get_agent()
            ships = self._get_ships()
            if ships and len(ships) == self.agent.ship_count:
                self.ships = ships
                return ships

        page, total = 1, 1
        while page <= total:
            r = self.api.fleet_api.get_my_ships(page=page, limit=20)
            total = r.meta.total / 20
            for s in r.data:
                self._set_ship(s)
            page += 1
        return r.data

    def get_system(self, system_symbol: str):
        system = self._get_system(system_symbol)
        if system:
            self.systems[system.symbol] = system
            return system
        r = self.api.systems_api.get_system(system_symbol)
        self._set_system(r.data)
        return r.data

    def get_waypoints(self, system: str):
        waypoints = self._get_waypoints(system)
        if waypoints:
            self.waypoints = waypoints
            return waypoints
        page = 1
        total = 1
        while page <= total:
            r = self.api.systems_api.get_system_waypoints(system, page=page, limit=20)
            total = r.meta.total / 20
            for waypoint in r.data:
                self._set_waypoint(system, waypoint)
            page += 1
        return r.data

    def get_shipyard(self, system, waypoint, force=False):
        if not force:
            shipyard = self._get_shipyard(waypoint)
            if shipyard:
                self.shipyards[shipyard.symbol] = shipyard
                return shipyard
        r = self.api.systems_api.get_shipyard(system, waypoint)
        self._set_shipyard(r.data)
        return r.data

    def dock(self, ship: Ship):
        r = self.api.fleet_api.dock_ship(ship.symbol)
        ship.nav = r.data.nav
        self._set_ship(ship)
        return r.data

    def orbit(self, ship: Ship):
        r = self.api.fleet_api.orbit_ship(ship.symbol)
        ship.nav = r.data.nav
        self._set_ship(ship)
        return r.data

    def navigate(self, ship: Ship | str, waypoint: Waypoint | str):
        if isinstance(ship, str):
            ship = self.ships[ship]
        if isinstance(waypoint, str):
            waypoint = self.waypoints[waypoint]
        if ship.nav.waypoint_symbol == waypoint.symbol:
            return None
        if ship.fuel.capacity < dist(self.waypoints[ship.nav.waypoint_symbol], waypoint):
            raise Exception("Not enough range")
        self.check_nav_status(ship, ShipNavStatus.IN_ORBIT)

        r = self.api.fleet_api.navigate_ship(ship.symbol, NavigateShipRequest(waypointSymbol=waypoint.symbol))
        r.data.nav.route.arrival - r.data.nav.route.departure_time
        ship.nav = r.data.nav
        ship.fuel = r.data.fuel
        self._set_ship(ship)
        self.logger.info(
            f"Ship {ship.symbol} is navigating to {waypoint.symbol} t={(ship.nav.route.arrival - ship.nav.route.departure_time).total_seconds():.2f}s fuel={ship.fuel.consumed.amount} d={dist(ship.nav.route.destination, ship.nav.route.origin):.2f}"
        )
        return r.data

    def buy_ship(self, waypoint: Waypoint | str, ship_type: ShipType | str):
        if isinstance(waypoint, str):
            waypoint = self.waypoints[waypoint]
        if isinstance(ship_type, str):
            ship_type = ShipType(ship_type)
        r = self.api.fleet_api.purchase_ship(PurchaseShipRequest(shipType=ship_type, waypointSymbol=waypoint.symbol))
        self._set_agent(r.data.agent)
        self._set_ship(r.data.ship)
        self.logger.info(f"Bought ship {r.data.ship.symbol} {r.data.transaction}")

        return r.data

    def get_market(self, system: System | str, waypoint: Waypoint | str, force=False):
        if isinstance(system, str):
            system = self.systems[system]
        if isinstance(waypoint, str):
            waypoint = self.waypoints[waypoint]
        if not force:
            market = self._get_market(waypoint)
            if market:
                self.markets[waypoint.symbol] = market
                return market
        r = self.api.systems_api.get_market(system.symbol, waypoint.symbol)
        self._set_market(r.data)
        return r.data

    def buy_good(self, ship: Ship | str, trade_good: TradeSymbol | str, units: int):
        if isinstance(ship, str):
            ship = self.ships[ship]
        if isinstance(trade_good, str):
            trade_good = TradeSymbol(trade_good)

        self.check_nav_status(ship, ShipNavStatus.DOCKED)

        r = self.api.fleet_api.purchase_cargo(ship.symbol, PurchaseCargoRequest(symbol=trade_good, units=units))
        self._set_agent(r.data.agent)
        self.ships[ship.symbol].cargo = r.data.cargo
        self._set_ship(self.ships[ship.symbol])
        self.logger.info(f"Bought {units} units of {trade_good} {r.data.transaction}")
        return r.data

    def sell_good(self, ship: Ship | str, trade_good: TradeSymbol | str, units: int):
        if isinstance(ship, str):
            ship = self.ships[ship]
        if isinstance(trade_good, str):
            trade_good = TradeSymbol(trade_good)

        self.check_nav_status(ship, ShipNavStatus.DOCKED)

        r = self.api.fleet_api.sell_cargo(ship.symbol, PurchaseCargoRequest(symbol=trade_good, units=units))
        self._set_agent(r.data.agent)
        self.ships[ship.symbol].cargo = r.data.cargo
        self._set_ship(self.ships[ship.symbol])
        self.logger.info(f"Sold {units} units of {trade_good} {r.data.transaction}")
        return r.data

    def refuel(self, ship: Ship | str, units: int | None = None, from_cargo: bool = False):
        if isinstance(ship, str):
            ship = self.ships[ship]
        self.check_nav_status(ship, ShipNavStatus.DOCKED)
        r = self.api.fleet_api.refuel_ship(ship.symbol, RefuelShipRequest(units=units, fromCargo=from_cargo))
        self._set_agent(r.data.agent)
        self.ships[ship.symbol].fuel = r.data.fuel
        self._set_ship(self.ships[ship.symbol])
        self.logger.info(f"Refueled {units} units {r.data.transaction}")
        return r.data

    def check_nav_status(self, ship: Ship, wanted_status: ShipNavStatus | str):
        ship = self.ships[ship.symbol]
        if ship.nav.status == ShipNavStatus.IN_TRANSIT:
            # add 1s to make sure we are not too early
            t = (ship.nav.route.arrival - datetime.now(timezone.utc)).total_seconds() + 1
            self.logger.info(f"Ship {ship.symbol} is in transit, waiting {t:.2f}s")
            time.sleep(t)
        if ship.nav.status != wanted_status:
            if wanted_status == ShipNavStatus.IN_ORBIT:
                self.orbit(ship)
            elif wanted_status == ShipNavStatus.DOCKED:
                self.dock(ship)
            else:
                raise Exception(f"What status did you want? You're imagining things: {wanted_status}")

    def check_cooldown(self, ship: Ship):
        if ship.cooldown.expiration and ship.cooldown.expiration > datetime.now(timezone.utc):
            t = (ship.cooldown.expiration - datetime.now(timezone.utc)).seconds
            self.logger.info(f"Ship {ship.symbol} is on cooldown, waiting {t:.2f}s")
            time.sleep(t)

    def filter_markets(self, good: TradeSymbol | str):
        if isinstance(good, str):
            good = TradeSymbol(good)

        have_good = []
        for market in self.markets.values():
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
