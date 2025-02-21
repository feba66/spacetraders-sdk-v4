import time
import redis

from spacetraders_sdk.openapi_client.models.cooldown import Cooldown
from spacetraders_sdk.openapi_client.models.ship_cargo import ShipCargo
from spacetraders_sdk.openapi_client.models.ship_fuel import ShipFuel

from .openapi_client import (
    Agent,
    Contract,
    Faction,
    FactionSymbol,
    Market,
    Ship,
    ShipNavStatus,
    ShipType,
    Shipyard,
    System,
    TradeSymbol,
    Waypoint,
    ShipNav,
)


class Storage:
    _meta: dict[str, float]

    _agent: Agent
    _credits: int
    _faction: Faction

    _contracts: dict[str, Contract]
    _markets: dict[str, Market]
    _ships: dict[str, Ship]
    _shipyards: dict[str, Shipyard]
    _systems: dict[str, System]
    _waypoints: dict[str, Waypoint]

    def __init__(self):
        self._contracts = {}
        self._markets = {}
        self._ships = {}
        self._shipyards = {}
        self._systems = {}
        self._waypoints = {}

        self._meta = {}

    # region Agent
    def set_agent(self, agent: Agent):
        self._agent = agent
        self._meta["agent"] = time.time()

    def get_agent(self) -> Agent:
        return self._agent

    def get_agent_meta(self) -> float:
        if "agent" not in self._meta:
            return None
        return self._meta["agent"]

    # endregion

    # region Ship
    def set_ship(self, ship: Ship):
        self._ships[ship.symbol] = ship
        self._meta[f"ship_{ship.symbol}"] = time.time()

    def get_ship(self, ship_id: str) -> Ship:
        if ship_id not in self._ships:
            return None
        return self._ships[ship_id]

    def get_ship_meta(self, ship_id: str) -> float:
        if f"ship_{ship_id}" not in self._meta:
            return None
        return self._meta[f"ship_{ship_id}"]

    def get_ships(self) -> list[Ship]:
        ships = list(self._ships.values())
        return ships, [self._meta[f"ship_{ship.symbol}"] for ship in ships]

    def set_ship_nav(self, ship: Ship | str, nav: ShipNav):
        pass

    def get_ship_nav(self, ship: Ship) -> ShipNav:
        pass

    def set_ship_cargo(self, ship: Ship | str, cargo: ShipCargo):
        pass

    def get_ship_cargo(self, ship: Ship) -> ShipCargo:
        pass

    def set_ship_cooldown(self, ship: Ship | str, cooldown: Cooldown):
        pass

    def get_ship_cooldown(self, ship: Ship) -> Cooldown:
        pass

    def set_ship_fuel(self, ship: Ship | str, fuel: ShipFuel):
        pass

    def get_ship_fuel(self, ship: Ship) -> ShipFuel:
        pass

    # endregion

    # region System
    def set_system(self, system: System):
        pass

    def get_system(self, system_symbol: str) -> System:
        pass

    def get_systems(self) -> list[System]:
        pass

    def set_waypoint(self, waypoint: Waypoint):
        pass

    def get_waypoint(self, waypoint_symbol: str) -> Waypoint:
        pass

    def get_waypoints(self) -> list[Waypoint]:
        pass

    def set_shipyard(self, shipyard: Shipyard):
        pass

    def get_shipyard(self, shipyard_symbol: str) -> Shipyard:
        pass

    def get_shipyards(self) -> list[Shipyard]:
        pass

    def set_market(self, market: Market):
        pass

    def get_market(self, market_symbol: str) -> Market:
        pass

    def get_market_meta(self, market_symbol: str) -> float:
        pass

    def get_markets(self) -> list[Market]:
        pass

    # endregion

    # region Faction
    def set_faction(self, faction: Faction):
        self._faction = faction
        self._meta["faction"] = time.time()

    def get_faction(self) -> tuple[Faction, float]:
        return self._faction, self._meta["faction"]

    # endregion

    # region Contract
    def set_contract(self, contract: Contract):
        self._contracts[contract.id] = contract
        self._meta[f"contract_{contract.id}"] = time.time()

    def get_contract(self, contract_id: str) -> tuple[Contract, float]:
        if contract_id not in self._contracts:
            return None
        return self._contracts[contract_id], self._meta[f"contract_{contract_id}"]

    def get_contracts(self) -> list[Contract]:
        contracts = list(self._contracts.values())
        return contracts, [self._meta[f"contract_{contract.id}"] for contract in contracts]

    # endregion

    # region lock

    def lock(self, key: str):
        pass

    def unlock(self, key: str):
        pass

    def is_locked(self, key: str) -> bool:
        pass

    # endregion


class RedisStorage(Storage):
    red: redis.Redis
    redis_prefix: str

    def __init__(self, redis_host: str, redis_port: int = 6379, redis_db: int = 0, redis_prefix: str = "SDKv4"):
        super().__init__()
        self.red = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.redis_prefix = redis_prefix

    # region Agent
    def set_agent(self, agent: Agent):
        t = time.time()
        self.red.set(f"{self.redis_prefix}:agent", agent.to_json())
        self.red.set(f"{self.redis_prefix}:meta:agent", f"{t}".encode("utf-8"))

    def get_agent(self) -> tuple[Agent, float]:
        agent = self.red.get(f"{self.redis_prefix}:agent")
        if agent:
            agent = Agent.from_json(agent)
            return agent
        return None

    # def set_credits(self, credits: int):
    #     t = time.time()
    #     self.red.set(f"{self.redis_prefix}:credits", credits)
    #     self.red.set(f"{self.redis_prefix}:meta:credits", f"{t}".encode("utf-8"))

    # def get_credits(self) -> int:
    #     return self.red.get(f"{self.redis_prefix}:credits")

    # endregion

    # region Ship
    def set_ship(self, ship: Ship):
        t = time.time()
        # super().set_ship(ship)
        self.red.set(f"{self.redis_prefix}:ship:{ship.symbol}", ship.to_json())
        self.red.set(f"{self.redis_prefix}:meta:ship:{ship.symbol}", f"{t}".encode("utf-8"))
        self.set_ship_nav(ship, ship.nav)
        self.set_ship_cargo(ship, ship.cargo)
        self.set_ship_cooldown(ship, ship.cooldown)
        self.set_ship_fuel(ship, ship.fuel)

    def get_ship(self, ship_id: str) -> Ship:
        ship = self.red.get(f"{self.redis_prefix}:ship:{ship_id}")
        if ship:
            ship = Ship.from_json(ship)
            nav = self.get_ship_nav(ship)
            cargo = self.get_ship_cargo(ship)
            cooldown = self.get_ship_cooldown(ship)
            fuel = self.get_ship_fuel(ship)
            ship.nav = nav
            ship.cargo = cargo
            ship.cooldown = cooldown
            ship.fuel = fuel
            return ship
        return None

    def set_ship_nav(self, ship: Ship | str, nav: ShipNav):
        if isinstance(ship, Ship):
            ship = ship.symbol
        t = time.time()
        self.red.set(f"{self.redis_prefix}:ship:{ship}_nav", nav.to_json())
        self.red.set(f"{self.redis_prefix}:meta:ship:{ship}_nav", f"{t}".encode("utf-8"))

    def get_ship_nav(self, ship: Ship | str) -> ShipNav:
        if isinstance(ship, Ship):
            ship = ship.symbol
        nav = self.red.get(f"{self.redis_prefix}:ship:{ship}_nav")
        if nav:
            nav = ShipNav.from_json(nav)
            return nav
        return None

    def set_ship_cargo(self, ship: Ship | str, cargo: ShipCargo):
        if isinstance(ship, Ship):
            ship = ship.symbol
        t = time.time()
        self.red.set(f"{self.redis_prefix}:ship:{ship}_cargo", cargo.to_json())
        self.red.set(f"{self.redis_prefix}:meta:ship:{ship}_cargo", f"{t}".encode("utf-8"))

    def get_ship_cargo(self, ship: Ship | str) -> ShipCargo:
        if isinstance(ship, Ship):
            ship = ship.symbol
        cargo = self.red.get(f"{self.redis_prefix}:ship:{ship}_cargo")
        if cargo:
            cargo = ShipCargo.from_json(cargo)
            return cargo
        return None

    def set_ship_cooldown(self, ship: Ship | str, cooldown: Cooldown):
        if isinstance(ship, Ship):
            ship = ship.symbol
        t = time.time()
        self.red.set(f"{self.redis_prefix}:ship:{ship}_cooldown", cooldown.to_json())
        self.red.set(f"{self.redis_prefix}:meta:ship:{ship}_cooldown", f"{t}".encode("utf-8"))

    def get_ship_cooldown(self, ship: Ship | str) -> Cooldown:
        if isinstance(ship, Ship):
            ship = ship.symbol
        cooldown = self.red.get(f"{self.redis_prefix}:ship:{ship}_cooldown")
        if cooldown:
            cooldown = Cooldown.from_json(cooldown)
            return cooldown
        return None

    def set_ship_fuel(self, ship: Ship | str, fuel: ShipFuel):
        if isinstance(ship, Ship):
            ship = ship.symbol
        t = time.time()
        self.red.set(f"{self.redis_prefix}:ship:{ship}_fuel", fuel.to_json())
        self.red.set(f"{self.redis_prefix}:meta:ship:{ship}_fuel", f"{t}".encode("utf-8"))

    def get_ship_fuel(self, ship: Ship | str) -> ShipFuel:
        if isinstance(ship, Ship):
            ship = ship.symbol
        fuel = self.red.get(f"{self.redis_prefix}:ship:{ship}_fuel")
        if fuel:
            fuel = ShipFuel.from_json(fuel)
            return fuel
        return None

    def get_ships(self) -> list[Ship]:
        ships = self.red.keys(f"{self.redis_prefix}:ship:*")
        if not ships:
            return None
        return [Ship.from_json(ship) for ship in self.red.mget([_ship for _ship in ships if not b"_" in _ship])]

    # endregion

    # region System
    def set_system(self, system: System):
        t = time.time()
        self.red.set(f"{self.redis_prefix}:system:{system.symbol}", system.to_json())
        self.red.set(f"{self.redis_prefix}:meta:system:{system.symbol}", f"{t}".encode("utf-8"))

    def get_system(self, system_symbol: str) -> System:
        system = self.red.get(f"{self.redis_prefix}:system:{system_symbol}")
        if system:
            system = System.from_json(system)
            return system
        return None

    def get_systems(self) -> list[System]:
        systems = self.red.keys(f"{self.redis_prefix}:system:*")
        if not systems:
            return None
        return [System.from_json(system) for system in self.red.mget([_system for _system in systems if not b"_" in _system])]

    def set_waypoint(self, waypoint: Waypoint):
        t = time.time()
        self.red.set(f"{self.redis_prefix}:waypoint:{waypoint.symbol}", waypoint.to_json())
        self.red.set(f"{self.redis_prefix}:meta:waypoint:{waypoint.symbol}", f"{t}".encode("utf-8"))

    def get_waypoint(self, waypoint_symbol: str) -> Waypoint:
        waypoint = self.red.get(f"{self.redis_prefix}:waypoint:{waypoint_symbol}")
        if waypoint:
            waypoint = Waypoint.from_json(waypoint)
            return waypoint
        return None

    def get_waypoints(self) -> list[Waypoint]:
        waypoints = self.red.keys(f"{self.redis_prefix}:waypoint:*")
        if not waypoints:
            return None
        return [
            Waypoint.from_json(waypoint)
            for waypoint in self.red.mget([_waypoint for _waypoint in waypoints if not b"_" in _waypoint])
        ]

    def set_shipyard(self, shipyard: Shipyard):
        t = time.time()
        self.red.set(f"{self.redis_prefix}:shipyard:{shipyard.symbol}", shipyard.to_json())
        self.red.set(f"{self.redis_prefix}:meta:shipyard:{shipyard.symbol}", f"{t}".encode("utf-8"))

    def get_shipyard(self, shipyard_symbol: str) -> Shipyard:
        shipyard = self.red.get(f"{self.redis_prefix}:shipyard:{shipyard_symbol}")
        if shipyard:
            shipyard = Shipyard.from_json(shipyard)
            return shipyard
        return None

    def get_shipyards(self) -> list[Shipyard]:
        shipyards = self.red.keys(f"{self.redis_prefix}:shipyard:*")
        if not shipyards:
            return None
        return [
            Shipyard.from_json(shipyard)
            for shipyard in self.red.mget([_shipyard for _shipyard in shipyards if not b"_" in _shipyard])
        ]

    def set_market(self, market: Market):
        t = time.time()
        self.red.set(f"{self.redis_prefix}:market:{market.symbol}", market.to_json())
        self.red.set(f"{self.redis_prefix}:meta:market:{market.symbol}", f"{t}".encode("utf-8"))

    def get_market(self, market_symbol: str) -> Market:
        market = self.red.get(f"{self.redis_prefix}:market:{market_symbol}")
        if market:
            market = Market.from_json(market)
            return market
        return None

    def get_market_meta(self, market_symbol: str) -> float:
        meta = self.red.get(f"{self.redis_prefix}:meta:market:{market_symbol}")
        if meta:
            return float(meta)
        return None

    def get_markets(self) -> list[Market]:
        markets = self.red.keys(f"{self.redis_prefix}:market:*")
        if not markets:
            return None
        return [Market.from_json(market) for market in self.red.mget([_market for _market in markets if not b"_" in _market])]

    # endregion

    # region lock

    def lock(self, key: str):
        r = self.red.set(f"{self.redis_prefix}:lock:{key}", "1", ex=7200, nx=True)
        return r

    def unlock(self, key: str):
        r = self.red.delete(f"{self.redis_prefix}:lock:{key}")
        return r

    def is_locked(self, key: str) -> bool:
        r = self.red.get(f"{self.redis_prefix}:lock:{key}")
        return r is not None

    # endregion
