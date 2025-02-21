from .openapi_client import Waypoint, WaypointTraitSymbol


def system_symbol_from_wp(from_wp):
    return from_wp.rsplit("-", 1)[0]


def waypoint_has_traits(waypoint: Waypoint, trait_symbols: list[WaypointTraitSymbol]) -> dict[WaypointTraitSymbol, bool]:
    has = {x: False for x in trait_symbols}
    for trait in waypoint.traits:
        if trait.symbol in trait_symbols:
            has[trait.symbol] = True
    return has
