# coding: utf-8

"""
    SpaceTraders API

    SpaceTraders is an open-universe game and learning platform that offers a set of HTTP endpoints to control a fleet of ships and explore a multiplayer universe.  The API is documented using [OpenAPI](https://github.com/SpaceTradersAPI/api-docs). You can send your first request right here in your browser to check the status of the game server.  ```json http {   \"method\": \"GET\",   \"url\": \"https://api.spacetraders.io/v2\", } ```  Unlike a traditional game, SpaceTraders does not have a first-party client or app to play the game. Instead, you can use the API to build your own client, write a script to automate your ships, or try an app built by the community.  We have a [Discord channel](https://discord.com/invite/jh6zurdWk5) where you cfroman share your projects, ask questions, and get help from other players.

    The version of the OpenAPI document: 2.0.0
    Contact: joel@spacetraders.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import List
from pydantic import BaseModel, Field, StrictInt, conlist, constr
from .system_faction import SystemFaction
from .system_type import SystemType
from .system_waypoint import SystemWaypoint


class System(BaseModel):
    """
    System
    """

    symbol: constr(strict=True, min_length=1) = Field(default=..., description="The symbol of the system.")
    sector_symbol: constr(strict=True, min_length=1) = Field(
        default=..., alias="sectorSymbol", description="The symbol of the sector."
    )
    type: SystemType = Field(...)
    x: StrictInt = Field(default=..., description="Relative position of the system in the sector in the x axis.")
    y: StrictInt = Field(default=..., description="Relative position of the system in the sector in the y axis.")
    waypoints: conlist(SystemWaypoint) = Field(default=..., description="Waypoints in this system.")
    factions: conlist(SystemFaction) = Field(default=..., description="Factions that control this system.")
    __properties = ["symbol", "sectorSymbol", "type", "x", "y", "waypoints", "factions"]

    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> System:
        """Create an instance of System from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in waypoints (list)
        _items = []
        if self.waypoints:
            for _item in self.waypoints:
                if _item:
                    _items.append(_item.to_dict())
            _dict["waypoints"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in factions (list)
        _items = []
        if self.factions:
            for _item in self.factions:
                if _item:
                    _items.append(_item.to_dict())
            _dict["factions"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> System:
        """Create an instance of System from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return System.parse_obj(obj)

        _obj = System.parse_obj(
            {
                "symbol": obj.get("symbol"),
                "sector_symbol": obj.get("sectorSymbol"),
                "type": obj.get("type"),
                "x": obj.get("x"),
                "y": obj.get("y"),
                "waypoints": (
                    [SystemWaypoint.from_dict(_item) for _item in obj.get("waypoints")]
                    if obj.get("waypoints") is not None
                    else None
                ),
                "factions": (
                    [SystemFaction.from_dict(_item) for _item in obj.get("factions")]
                    if obj.get("factions") is not None
                    else None
                ),
            }
        )
        return _obj
