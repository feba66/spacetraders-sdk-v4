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


from typing import Union
from pydantic import BaseModel, Field, StrictStr, confloat, conint, validator
from .ship_requirements import ShipRequirements


class ShipFrame(BaseModel):
    """
    The frame of the ship. The frame determines the number of modules and mounting points of the ship, as well as base fuel capacity. As the condition of the frame takes more wear, the ship will become more sluggish and less maneuverable.  # noqa: E501
    """

    symbol: StrictStr = Field(default=..., description="Symbol of the frame.")
    name: StrictStr = Field(default=..., description="Name of the frame.")
    description: StrictStr = Field(default=..., description="Description of the frame.")
    condition: Union[confloat(le=1, ge=0, strict=True), conint(le=1, ge=0, strict=True)] = Field(
        default=...,
        description="The repairable condition of a component. A value of 0 indicates the component needs significant repairs, while a value of 1 indicates the component is in near perfect condition. As the condition of a component is repaired, the overall integrity of the component decreases.",
    )
    integrity: Union[confloat(le=1, ge=0, strict=True), conint(le=1, ge=0, strict=True)] = Field(
        default=...,
        description="The overall integrity of the component, which determines the performance of the component. A value of 0 indicates that the component is almost completely degraded, while a value of 1 indicates that the component is in near perfect condition. The integrity of the component is non-repairable, and represents permanent wear over time.",
    )
    module_slots: conint(strict=True, ge=0) = Field(
        default=...,
        alias="moduleSlots",
        description="The amount of slots that can be dedicated to modules installed in the ship. Each installed module take up a number of slots, and once there are no more slots, no new modules can be installed.",
    )
    mounting_points: conint(strict=True, ge=0) = Field(
        default=...,
        alias="mountingPoints",
        description="The amount of slots that can be dedicated to mounts installed in the ship. Each installed mount takes up a number of points, and once there are no more points remaining, no new mounts can be installed.",
    )
    fuel_capacity: conint(strict=True, ge=0) = Field(
        default=...,
        alias="fuelCapacity",
        description="The maximum amount of fuel that can be stored in this ship. When refueling, the ship will be refueled to this amount.",
    )
    requirements: ShipRequirements = Field(...)
    __properties = [
        "symbol",
        "name",
        "description",
        "condition",
        "integrity",
        "moduleSlots",
        "mountingPoints",
        "fuelCapacity",
        "requirements",
    ]

    @validator("symbol")
    def symbol_validate_enum(cls, value):
        """Validates the enum"""
        if value not in (
            "FRAME_PROBE",
            "FRAME_DRONE",
            "FRAME_INTERCEPTOR",
            "FRAME_RACER",
            "FRAME_FIGHTER",
            "FRAME_FRIGATE",
            "FRAME_SHUTTLE",
            "FRAME_EXPLORER",
            "FRAME_MINER",
            "FRAME_LIGHT_FREIGHTER",
            "FRAME_HEAVY_FREIGHTER",
            "FRAME_TRANSPORT",
            "FRAME_DESTROYER",
            "FRAME_CRUISER",
            "FRAME_CARRIER",
        ):
            raise ValueError(
                "must be one of enum values ('FRAME_PROBE', 'FRAME_DRONE', 'FRAME_INTERCEPTOR', 'FRAME_RACER', 'FRAME_FIGHTER', 'FRAME_FRIGATE', 'FRAME_SHUTTLE', 'FRAME_EXPLORER', 'FRAME_MINER', 'FRAME_LIGHT_FREIGHTER', 'FRAME_HEAVY_FREIGHTER', 'FRAME_TRANSPORT', 'FRAME_DESTROYER', 'FRAME_CRUISER', 'FRAME_CARRIER')"
            )
        return value

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
    def from_json(cls, json_str: str) -> ShipFrame:
        """Create an instance of ShipFrame from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of requirements
        if self.requirements:
            _dict["requirements"] = self.requirements.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ShipFrame:
        """Create an instance of ShipFrame from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ShipFrame.parse_obj(obj)

        _obj = ShipFrame.parse_obj(
            {
                "symbol": obj.get("symbol"),
                "name": obj.get("name"),
                "description": obj.get("description"),
                "condition": obj.get("condition"),
                "integrity": obj.get("integrity"),
                "module_slots": obj.get("moduleSlots"),
                "mounting_points": obj.get("mountingPoints"),
                "fuel_capacity": obj.get("fuelCapacity"),
                "requirements": (
                    ShipRequirements.from_dict(obj.get("requirements")) if obj.get("requirements") is not None else None
                ),
            }
        )
        return _obj
