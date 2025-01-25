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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictInt, conlist, constr

from spacetraders_sdk.json import default
from .chart import Chart
from .waypoint_faction import WaypointFaction
from .waypoint_modifier import WaypointModifier
from .waypoint_orbital import WaypointOrbital
from .waypoint_trait import WaypointTrait
from .waypoint_type import WaypointType


class Waypoint(BaseModel):
    """
    A waypoint is a location that ships can travel to such as a Planet, Moon or Space Station.  # noqa: E501
    """

    symbol: constr(strict=True, min_length=1) = Field(default=..., description="The symbol of the waypoint.")
    type: WaypointType = Field(...)
    system_symbol: constr(strict=True, min_length=1) = Field(
        default=..., alias="systemSymbol", description="The symbol of the system."
    )
    x: StrictInt = Field(
        default=...,
        description="Relative position of the waypoint on the system's x axis. This is not an absolute position in the universe.",
    )
    y: StrictInt = Field(
        default=...,
        description="Relative position of the waypoint on the system's y axis. This is not an absolute position in the universe.",
    )
    orbitals: conlist(WaypointOrbital) = Field(default=..., description="Waypoints that orbit this waypoint.")
    orbits: Optional[constr(strict=True, min_length=1)] = Field(
        default=None,
        description="The symbol of the parent waypoint, if this waypoint is in orbit around another waypoint. Otherwise this value is undefined.",
    )
    faction: Optional[WaypointFaction] = None
    traits: conlist(WaypointTrait) = Field(default=..., description="The traits of the waypoint.")
    modifiers: Optional[conlist(WaypointModifier)] = Field(default=None, description="The modifiers of the waypoint.")
    chart: Optional[Chart] = None
    is_under_construction: StrictBool = Field(
        default=..., alias="isUnderConstruction", description="True if the waypoint is under construction."
    )
    __properties = [
        "symbol",
        "type",
        "systemSymbol",
        "x",
        "y",
        "orbitals",
        "orbits",
        "faction",
        "traits",
        "modifiers",
        "chart",
        "isUnderConstruction",
    ]

    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict(), default=default)

    @classmethod
    def from_json(cls, json_str: str) -> Waypoint:
        """Create an instance of Waypoint from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in orbitals (list)
        _items = []
        if self.orbitals:
            for _item in self.orbitals:
                if _item:
                    _items.append(_item.to_dict())
            _dict["orbitals"] = _items
        # override the default output from pydantic by calling `to_dict()` of faction
        if self.faction:
            _dict["faction"] = self.faction.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in traits (list)
        _items = []
        if self.traits:
            for _item in self.traits:
                if _item:
                    _items.append(_item.to_dict())
            _dict["traits"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in modifiers (list)
        _items = []
        if self.modifiers:
            for _item in self.modifiers:
                if _item:
                    _items.append(_item.to_dict())
            _dict["modifiers"] = _items
        # override the default output from pydantic by calling `to_dict()` of chart
        if self.chart:
            _dict["chart"] = self.chart.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Waypoint:
        """Create an instance of Waypoint from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Waypoint.parse_obj(obj)

        _obj = Waypoint.parse_obj(
            {
                "symbol": obj.get("symbol"),
                "type": obj.get("type"),
                "system_symbol": obj.get("systemSymbol"),
                "x": obj.get("x"),
                "y": obj.get("y"),
                "orbitals": (
                    [WaypointOrbital.from_dict(_item) for _item in obj.get("orbitals")]
                    if obj.get("orbitals") is not None
                    else None
                ),
                "orbits": obj.get("orbits"),
                "faction": WaypointFaction.from_dict(obj.get("faction")) if obj.get("faction") is not None else None,
                "traits": (
                    [WaypointTrait.from_dict(_item) for _item in obj.get("traits")] if obj.get("traits") is not None else None
                ),
                "modifiers": (
                    [WaypointModifier.from_dict(_item) for _item in obj.get("modifiers")]
                    if obj.get("modifiers") is not None
                    else None
                ),
                "chart": Chart.from_dict(obj.get("chart")) if obj.get("chart") is not None else None,
                "is_under_construction": obj.get("isUnderConstruction"),
            }
        )
        return _obj
