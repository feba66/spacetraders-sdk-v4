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


from pydantic import BaseModel, Field, StrictStr, validator


class ShipConditionEvent(BaseModel):
    """
    An event that represents damage or wear to a ship's reactor, frame, or engine, reducing the condition of the ship.  # noqa: E501
    """

    symbol: StrictStr = Field(...)
    component: StrictStr = Field(...)
    name: StrictStr = Field(default=..., description="The name of the event.")
    description: StrictStr = Field(default=..., description="A description of the event.")
    __properties = ["symbol", "component", "name", "description"]

    @validator("symbol")
    def symbol_validate_enum(cls, value):
        """Validates the enum"""
        if value not in (
            "REACTOR_OVERLOAD",
            "ENERGY_SPIKE_FROM_MINERAL",
            "SOLAR_FLARE_INTERFERENCE",
            "COOLANT_LEAK",
            "POWER_DISTRIBUTION_FLUCTUATION",
            "MAGNETIC_FIELD_DISRUPTION",
            "HULL_MICROMETEORITE_STRIKES",
            "STRUCTURAL_STRESS_FRACTURES",
            "CORROSIVE_MINERAL_CONTAMINATION",
            "THERMAL_EXPANSION_MISMATCH",
            "VIBRATION_DAMAGE_FROM_DRILLING",
            "ELECTROMAGNETIC_FIELD_INTERFERENCE",
            "IMPACT_WITH_EXTRACTED_DEBRIS",
            "FUEL_EFFICIENCY_DEGRADATION",
            "COOLANT_SYSTEM_AGEING",
            "DUST_MICROABRASIONS",
            "THRUSTER_NOZZLE_WEAR",
            "EXHAUST_PORT_CLOGGING",
            "BEARING_LUBRICATION_FADE",
            "SENSOR_CALIBRATION_DRIFT",
            "HULL_MICROMETEORITE_DAMAGE",
            "SPACE_DEBRIS_COLLISION",
            "THERMAL_STRESS",
            "VIBRATION_OVERLOAD",
            "PRESSURE_DIFFERENTIAL_STRESS",
            "ELECTROMAGNETIC_SURGE_EFFECTS",
            "ATMOSPHERIC_ENTRY_HEAT",
        ):
            raise ValueError(
                "must be one of enum values ('REACTOR_OVERLOAD', 'ENERGY_SPIKE_FROM_MINERAL', 'SOLAR_FLARE_INTERFERENCE', 'COOLANT_LEAK', 'POWER_DISTRIBUTION_FLUCTUATION', 'MAGNETIC_FIELD_DISRUPTION', 'HULL_MICROMETEORITE_STRIKES', 'STRUCTURAL_STRESS_FRACTURES', 'CORROSIVE_MINERAL_CONTAMINATION', 'THERMAL_EXPANSION_MISMATCH', 'VIBRATION_DAMAGE_FROM_DRILLING', 'ELECTROMAGNETIC_FIELD_INTERFERENCE', 'IMPACT_WITH_EXTRACTED_DEBRIS', 'FUEL_EFFICIENCY_DEGRADATION', 'COOLANT_SYSTEM_AGEING', 'DUST_MICROABRASIONS', 'THRUSTER_NOZZLE_WEAR', 'EXHAUST_PORT_CLOGGING', 'BEARING_LUBRICATION_FADE', 'SENSOR_CALIBRATION_DRIFT', 'HULL_MICROMETEORITE_DAMAGE', 'SPACE_DEBRIS_COLLISION', 'THERMAL_STRESS', 'VIBRATION_OVERLOAD', 'PRESSURE_DIFFERENTIAL_STRESS', 'ELECTROMAGNETIC_SURGE_EFFECTS', 'ATMOSPHERIC_ENTRY_HEAT')"
            )
        return value

    @validator("component")
    def component_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ("FRAME", "REACTOR", "ENGINE"):
            raise ValueError("must be one of enum values ('FRAME', 'REACTOR', 'ENGINE')")
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
    def from_json(cls, json_str: str) -> ShipConditionEvent:
        """Create an instance of ShipConditionEvent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ShipConditionEvent:
        """Create an instance of ShipConditionEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ShipConditionEvent.parse_obj(obj)

        _obj = ShipConditionEvent.parse_obj(
            {
                "symbol": obj.get("symbol"),
                "component": obj.get("component"),
                "name": obj.get("name"),
                "description": obj.get("description"),
            }
        )
        return _obj
