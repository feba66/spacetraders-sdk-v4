# coding: utf-8

"""
    SpaceTraders API

    SpaceTraders is an open-universe game and learning platform that offers a set of HTTP endpoints to control a fleet of ships and explore a multiplayer universe.  The API is documented using [OpenAPI](https://github.com/SpaceTradersAPI/api-docs). You can send your first request right here in your browser to check the status of the game server.  ```json http {   \"method\": \"GET\",   \"url\": \"https://api.spacetraders.io/v2\", } ```  Unlike a traditional game, SpaceTraders does not have a first-party client or app to play the game. Instead, you can use the API to build your own client, write a script to automate your ships, or try an app built by the community.  We have a [Discord channel](https://discord.com/invite/jh6zurdWk5) where you can share your projects, ask questions, and get help from other players.   

    The version of the OpenAPI document: 2.0.0
    Contact: joel@spacetraders.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class FactionSymbol(str, Enum):
    """
    The symbol of the faction.
    """

    """
    allowed enum values
    """
    COSMIC = 'COSMIC'
    VOID = 'VOID'
    GALACTIC = 'GALACTIC'
    QUANTUM = 'QUANTUM'
    DOMINION = 'DOMINION'
    ASTRO = 'ASTRO'
    CORSAIRS = 'CORSAIRS'
    OBSIDIAN = 'OBSIDIAN'
    AEGIS = 'AEGIS'
    UNITED = 'UNITED'
    SOLITARY = 'SOLITARY'
    COBALT = 'COBALT'
    OMEGA = 'OMEGA'
    ECHO = 'ECHO'
    LORDS = 'LORDS'
    CULT = 'CULT'
    ANCIENTS = 'ANCIENTS'
    SHADOW = 'SHADOW'
    ETHEREAL = 'ETHEREAL'

    @classmethod
    def from_json(cls, json_str: str) -> FactionSymbol:
        """Create an instance of FactionSymbol from a JSON string"""
        return FactionSymbol(json.loads(json_str))


