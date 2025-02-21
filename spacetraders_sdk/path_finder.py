from enum import Enum
from .astar import dist, AStarNode, CostNode, AStarSearch
from spacetraders_sdk.util import system_symbol_from_wp, waypoint_has_traits
from .openapi_client import Waypoint, WaypointTraitSymbol, ShipNavFlightMode
from .storage import Storage


multmap_nav = {
    ShipNavFlightMode.CRUISE: 25,
    ShipNavFlightMode.STEALTH: 50,
    ShipNavFlightMode.DRIFT: 250,
    ShipNavFlightMode.BURN: 12.5,
}


class Priority(Enum):
    DISTANCE = "distance"
    FUEL = "fuel"
    TIME = "time"


class Options:
    radius: int
    flight_mode: ShipNavFlightMode
    engine_speed: int
    priority: str
    system: str

    def __init__(self, radius: int, flight_mode: ShipNavFlightMode, engine_speed: int, priority: str, system: str):
        self.radius = radius
        self.flight_mode = flight_mode
        self.engine_speed = engine_speed
        self.priority = priority
        self.system = system


class PathFinder:
    storage: Storage

    nodelists: dict
    cache: dict

    def __init__(self, storage: Storage):
        self.storage = storage
        self.nodelists = {}
        self.cache = {}

    def create_nodelist(self, options: Options):
        system = self.storage.get_system(options.system)
        if system is None:
            raise ValueError("System not found")
        waypoints = [wp for wp in self.storage.get_waypoints() if wp.system_symbol == options.system]
        if waypoints is None:
            raise ValueError("Waypoints not found")

        markets = []
        for wp in waypoints:
            res = waypoint_has_traits(wp, [WaypointTraitSymbol.MARKETPLACE])
            if res[WaypointTraitSymbol.MARKETPLACE]:
                markets.append(wp)

        node_list = []
        for wp in markets:
            connections = []
            for wp2 in markets:
                if wp.symbol != wp2.symbol and dist(wp, wp2) < options.radius:
                    d = max(1, round(dist(wp, wp2)))
                    if options.priority == Priority.DISTANCE:
                        cost = d
                    elif options.priority == Priority.FUEL:
                        if options.flight_mode == ShipNavFlightMode.CRUISE or options.flight_mode == ShipNavFlightMode.STEALTH:
                            cost = d
                        elif options.flight_mode == ShipNavFlightMode.DRIFT:
                            cost = 1
                        elif options.flight_mode == ShipNavFlightMode.BURN:
                            cost = d * 2
                        else:
                            raise ValueError("Invalid flight_mode")
                    elif options.priority == Priority.TIME:
                        if d == 0:
                            cost = 15
                        else:
                            cost = round((d / options.engine_speed) * multmap_nav[options.flight_mode] + 15)
                    else:
                        cost = 1
                    connections.append(CostNode(wp2.symbol, max(1, cost)))
            node_list.append(AStarNode(wp.symbol, connections, wp.x, wp.y))
        return node_list

    def get_route(self, start: str, goal: str, options: Options):
        if system_symbol_from_wp(start) != system_symbol_from_wp(goal):
            raise ValueError("Start and goal must be in the same system")
        if options.priority == Priority.FUEL and options.flight_mode is None:
            raise ValueError("flight_mode required for fuel priority")
        if options.priority == Priority.TIME and (options.flight_mode is None or options.engine_speed is None):
            raise ValueError("flight_mode and engine_speed required for time priority")

        if (start, goal, options) in self.cache:
            return self.cache[(start, goal, options)]

        if options not in self.nodelists:
            nodelist = self.nodelists[options] = self.create_nodelist(options)
        else:
            nodelist = self.nodelists[options]

        res = AStarSearch(start, goal, nodelist)
        self.cache[(start, goal, options)] = res
        return res
