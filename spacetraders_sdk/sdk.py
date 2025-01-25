from datetime import datetime, timezone
import os
import time
import logging
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

    def __init__(self, token: str | None = None, host: str | None = None):
        self.api = API()
        self.systems = {}
        self.ships = {}
        self.contracts = {}
        self.waypoints = {}
        self.shipyards = {}
        self.markets = {}

        self.logger = logging.getLogger("sdk")
        logging.basicConfig(filename="sdk.log", level=logging.INFO)

        self.api.config = Configuration(
            host="https://api.spacetraders.io/v2" if host is None else host
        )
        if token is not None:
            self.api.config.access_token = token

        self.api.client = ApiClient(self.api.config)

        self.api.agents_api = AgentsApi(self.api.client)
        self.api.fleet_api = FleetApi(self.api.client)
        self.api.default_api = DefaultApi(self.api.client)
        self.api.systems_api = SystemsApi(self.api.client)
        self.api.contracts_api = ContractsApi(self.api.client)
        self.api.factions_api = FactionsApi(self.api.client)

    def register(
        self, username: str, faction: FactionSymbol | str = FactionSymbol.ASTRO
    ):  # noqa
        if isinstance(faction, str):
            faction = FactionSymbol(faction)
        r = self.api.default_api.register(
            RegisterRequest(symbol=username, faction=faction)
        )

        self.agent = r.data.agent
        self.contracts = {r.data.contract.id: r.data.contract}
        self.faction = r.data.faction
        r.data.ship
        self.token = r.data.token
        self.logger.info(f"Registered as {self.agent.symbol} with token {r.data.token}")
        return r.data

    def get_agent(self):
        r = self.api.agents_api.get_my_agent()
        self.agent = r.data
        return r.data

    def get_contracts(self):
        page, total = 1, 1
        while page <= total:
            r = self.api.contracts_api.get_contracts(page=page, limit=20)
            total = r.meta.total / 20
            for c in r.data:
                self.contracts[c.id] = c
            page += 1
        return r.data

    def accept_contract(self, contract: Contract | str):
        if isinstance(contract, str):
            contract = self.contracts[contract]
        r = self.api.contracts_api.accept_contract(contract.id)
        self.agent = r.data.agent
        self.contracts[contract.id] = r.data.contract
        self.logger.info(f"Accepted contract {contract.id}")
        return r.data

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
            DeliverContractRequest(
                shipSymbol=ship.symbol, tradeSymbol=trade_symbol, units=units
            ),
        )
        self.contracts[contract.id] = r.data.contract
        self.ships[ship.symbol].cargo = r.data.cargo
        self.logger.info(f"Delivered contract {contract.id} {units}x {trade_symbol}")
        return r.data

    def fulfill_contract(self, contract: Contract | str):
        if isinstance(contract, str):
            contract = self.contracts[contract]
        r = self.api.contracts_api.fulfill_contract(contract.id)
        self.agent = r.data.agent
        self.contracts[contract.id] = r.data.contract
        self.logger.info(f"Fulfilled contract {contract.id}")
        return r.data

    def negotiate_contract(self, ship: Ship | str):
        if isinstance(ship, str):
            ship = self.ships[ship]
        r = self.api.fleet_api.negotiate_contract(ship.symbol)
        self.contracts[r.data.contract.id] = r.data.contract
        self.logger.info(f"Negotiated contract {r.data.contract.id}")
        return r.data

    def get_ships(self):
        page, total = 1, 1
        while page <= total:
            r = self.api.fleet_api.get_my_ships(page=page, limit=20)
            total = r.meta.total / 20
            for s in r.data:
                self.ships[s.symbol] = s
            page += 1
        return r.data

    def get_system(self, system: str):
        r = self.api.systems_api.get_system(system)
        self.systems[r.data.symbol] = r.data
        return r.data

    def get_waypoints(self, system: str):
        page = 1
        total = 1
        while page <= total:
            r = self.api.systems_api.get_system_waypoints(system, page=page, limit=20)
            total = r.meta.total / 20
            for waypoint in r.data:
                self.waypoints[waypoint.symbol] = waypoint
            page += 1
        return r.data

    def get_shipyard(self, system, waypoint):
        r = self.api.systems_api.get_shipyard(system, waypoint)
        self.shipyards[r.data.symbol] = r.data
        return r.data

    def dock(self, ship: Ship):
        r = self.api.fleet_api.dock_ship(ship.symbol)
        ship.nav = r.data.nav
        return r.data

    def orbit(self, ship: Ship):
        r = self.api.fleet_api.orbit_ship(ship.symbol)
        ship.nav = r.data.nav
        return r.data

    def navigate(self, ship: Ship | str, waypoint: Waypoint | str):
        if isinstance(ship, str):
            ship = self.ships[ship]
        if isinstance(waypoint, str):
            waypoint = self.waypoints[waypoint]
        if ship.nav.waypoint_symbol == waypoint.symbol:
            return None

        if ship.nav.status != ShipNavStatus.IN_ORBIT:
            self.orbit(ship)
        if ship.cooldown.expiration and ship.cooldown.expiration > datetime.now(
            timezone.utc
        ):
            self.logger.info(f"Ship {ship.symbol} is on cooldown")
            time.sleep((ship.cooldown.expiration - datetime.now(timezone.utc)).seconds)
        r = self.api.fleet_api.navigate_ship(
            ship.symbol, NavigateShipRequest(waypointSymbol=waypoint.symbol)
        )
        r.data.nav.route.arrival - r.data.nav.route.departure_time
        ship.nav = r.data.nav
        ship.fuel = r.data.fuel
        return r.data

    def buy_ship(self, waypoint: Waypoint | str, ship_type: ShipType | str):
        if isinstance(waypoint, str):
            waypoint = self.waypoints[waypoint]
        if isinstance(ship_type, str):
            ship_type = ShipType(ship_type)
        r = self.api.fleet_api.purchase_ship(
            PurchaseShipRequest(shipType=ship_type, waypointSymbol=waypoint.symbol)
        )
        self.agent = r.data.agent
        self.ships[r.data.ship.symbol] = r.data.ship
        self.logger.info(f"Bought ship {r.data.ship.symbol} {r.data.transaction}")

        return r.data

    def get_market(self, system: System | str, waypoint: Waypoint | str):
        if isinstance(system, str):
            system = self.systems[system]
        if isinstance(waypoint, str):
            waypoint = self.waypoints[waypoint]
        r = self.api.systems_api.get_market(system.symbol, waypoint.symbol)
        self.markets[waypoint.symbol] = r.data
        return r.data

    def buy_good(self, ship: Ship | str, trade_good: TradeSymbol | str, units: int):
        if isinstance(ship, str):
            ship = self.ships[ship]
        if isinstance(trade_good, str):
            trade_good = TradeSymbol(trade_good)

        self.check_nav_status(ship, ShipNavStatus.DOCKED)

        r = self.api.fleet_api.purchase_cargo(
            ship.symbol, PurchaseCargoRequest(symbol=trade_good, units=units)
        )
        self.agent = r.data.agent
        self.ships[ship.symbol].cargo = r.data.cargo
        self.logger.info(f"Bought {units} units of {trade_good} {r.data.transaction}")
        return r.data

    def refuel(
        self, ship: Ship | str, units: int | None = None, from_cargo: bool = False
    ):
        if isinstance(ship, str):
            ship = self.ships[ship]
        r = self.api.fleet_api.refuel_ship(
            ship.symbol, RefuelShipRequest(units=units, fromCargo=from_cargo)
        )
        self.agent = r.data.agent
        self.ships[ship.symbol].fuel = r.data.fuel
        self.logger.info(f"Refueled {units} units {r.data.transaction}")
        return r.data

    def check_nav_status(self, ship: Ship, wanted_status: ShipNavStatus | str):
        if ship.nav.status == ShipNavStatus.IN_TRANSIT:
            t = (ship.nav.route.arrival - datetime.now(timezone.utc)).total_seconds()
            self.logger.info(f"Ship {ship.symbol} is in transit, waiting {t:.2f}s")
            time.sleep(t)
        if ship.nav.status != wanted_status:
            if ship.nav.status == ShipNavStatus.DOCKED:
                self.orbit(ship)
            if ship.nav.status == ShipNavStatus.IN_ORBIT:
                self.dock(ship)

    def check_cooldown(self, ship: Ship):
        if ship.cooldown.expiration and ship.cooldown.expiration > datetime.now(
            timezone.utc
        ):
            t = (ship.cooldown.expiration - datetime.now(timezone.utc)).seconds
            self.logger.info(f"Ship {ship.symbol} is on cooldown, waiting {t:.2f}s")
            time.sleep(t)

    class Helpers:
        @staticmethod
        def dist(a: Waypoint | System, b: Waypoint | System):
            return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5
