from astar import dist, AStarNode, CostNode, AStarSearch
from spacetraders_sdk import SDK
from config import TOKEN, BASE_URL
from fastapi import FastAPI
import uvicorn

from spacetraders_sdk.openapi_client.models.waypoint import Waypoint
from spacetraders_sdk.openapi_client.models.waypoint_trait_symbol import WaypointTraitSymbol


nodelists: dict[tuple[str, str, str, int, int], list[AStarNode]] = {}
"""dict of (system_symbol, priority, flight_mode, engine_speed, range) -> nodelist"""

cache: dict[tuple[str, str, str, str, str, int, int], CostNode] = {}
"""dict of (system_symbol, from, to, priority, flight_mode, engine_speed, range) -> route"""

sdk = SDK(TOKEN, BASE_URL)

multmap_nav = {"CRUISE": 10, "STEALTH": 20, "DRIFT": 100, "BURN": 5}


def gen_node_list(system_symbol: str, max_range: int, priority: str, flight_mode: str = None, engine_speed: int = None):
    global sdk
    sdk.get_system(system_symbol)
    res = sdk.get_waypoints(system_symbol)

    for wp in res:
        wp: Waypoint
        is_market = False
        for trait in wp.traits:
            if trait.symbol == WaypointTraitSymbol.MARKETPLACE:
                is_market = True
        if is_market:
            sdk.get_market(wp.system_symbol, wp.symbol)

    markets = [m.symbol for m in sdk.markets.values()]
    node_list = []

    wps = [wp for wp in sdk.systems[system_symbol].waypoints if wp.symbol in markets]
    for wp in wps:
        connections = []
        for wp2 in wps:
            if wp.symbol != wp2.symbol and dist(wp, wp2) < max_range:
                d = max(1, round(dist(wp, wp2)))
                if priority == "distance":
                    cost = d
                elif priority == "fuel":
                    if flight_mode is None:
                        return {"error": "flight_mode required for fuel priority"}
                    if flight_mode == "CRUISE" or flight_mode == "STEALTH":
                        cost = d
                    elif flight_mode == "DRIFT":
                        cost = 1
                    elif flight_mode == "BURN":
                        cost = d * 2
                    else:
                        return {"error": "Invalid flight_mode"}
                elif priority == "time":
                    if flight_mode is None or engine_speed is None:
                        return {"error": "flight_mode and engine_speed required for time priority"}
                    if d == 0:
                        cost = 15
                    cost = round((d / engine_speed) * multmap_nav[flight_mode] + 15)
                else:
                    cost = 1
                connections.append(CostNode(wp2.symbol, max(1, cost)))
        node_list.append(AStarNode(wp.symbol, connections, wp.x, wp.y))

    return node_list


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/waypoints")
def read_waypoints(
    from_wp: str | None = None,
    to_wp: str | None = None,
    distance: int | None = None,
    priority: str = "distance",
    flight_mode: str | None = None,
    engine_speed: int | None = None,
):
    global nodelists, cache

    if from_wp is None or to_wp is None or distance is None:
        return {"error": "from_wp, to_wp and distance are required"}

    system_symbol = from_wp.rsplit("-", 1)[0]
    if system_symbol != to_wp.rsplit("-", 1)[0]:
        return {"error": "from_wp and to_wp must be in the same system"}
    priority = priority.lower()
    if priority not in ["distance", "fuel", "time"]:
        return {"error": "Invalid priority"}

    if priority == "fuel" and flight_mode is None:
        return {"error": "flight_mode required for fuel priority"}

    if priority == "time" and (flight_mode is None or engine_speed is None):
        return {"error": "flight_mode and engine_speed required for time priority"}
    flight_mode = flight_mode.upper()

    cache_tuple = (
        system_symbol,
        from_wp,
        to_wp,
        priority,
        flight_mode,
        engine_speed,
        distance,
    )
    if cache_tuple in cache:
        return {"res": cache[cache_tuple], "cached": True}
    nodelist_tuple = (
        system_symbol,
        priority,
        flight_mode,
        engine_speed,
        distance,
    )
    if nodelist_tuple not in nodelists:
        node_list = gen_node_list(system_symbol, distance, priority, flight_mode, engine_speed)
        if "error" in node_list:
            return node_list
        nodelists[nodelist_tuple] = node_list
    else:
        node_list = nodelists[nodelist_tuple]

    res = AStarSearch(from_wp, to_wp, node_list)
    cache[cache_tuple] = res
    return {"res": res}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6600)
