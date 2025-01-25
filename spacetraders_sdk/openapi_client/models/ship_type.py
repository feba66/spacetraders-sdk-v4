# coding: utf-8

"""
    SpaceTraders API

    SpaceTraders is an open-universe game and learning platform that offers a set of HTTP endpoints to control a fleet of ships and explore a multiplayer universe.  The API is documented using [OpenAPI](https://github.com/SpaceTradersAPI/api-docs). You can send your first request right here in your browser to check the status of the game server.  ```json http {   \"method\": \"GET\",   \"url\": \"https://api.spacetraders.io/v2\", } ```  Unlike a traditional game, SpaceTraders does not have a first-party client or app to play the game. Instead, you can use the API to build your own client, write a script to automate your ships, or try an app built by the community.  We have a [Discord channel](https://discord.com/invite/jh6zurdWk5) where you cfroman share your projects, ask questions, and get help from other players.

    The version of the OpenAPI document: 2.0.0
    Contact: joel@spacetraders.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg


class ShipType(str, Enum):
    """
    Type of ship
    """

    """
    allowed enum values
    """
    SHIP_PROBE = "SHIP_PROBE"
    SHIP_MINING_DRONE = "SHIP_MINING_DRONE"
    SHIP_SIPHON_DRONE = "SHIP_SIPHON_DRONE"
    SHIP_INTERCEPTOR = "SHIP_INTERCEPTOR"
    SHIP_LIGHT_HAULER = "SHIP_LIGHT_HAULER"
    SHIP_COMMAND_FRIGATE = "SHIP_COMMAND_FRIGATE"
    SHIP_EXPLORER = "SHIP_EXPLORER"
    SHIP_HEAVY_FREIGHTER = "SHIP_HEAVY_FREIGHTER"
    SHIP_LIGHT_SHUTTLE = "SHIP_LIGHT_SHUTTLE"
    SHIP_ORE_HOUND = "SHIP_ORE_HOUND"
    SHIP_REFINING_FREIGHTER = "SHIP_REFINING_FREIGHTER"
    SHIP_SURVEYOR = "SHIP_SURVEYOR"

    @classmethod
    def from_json(cls, json_str: str) -> ShipType:
        """Create an instance of ShipType from a JSON string"""
        return ShipType(json.loads(json_str))
