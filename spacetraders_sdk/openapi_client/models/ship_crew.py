# coding: utf-8

"""
    SpaceTraders API

    SpaceTraders is an open-universe game and learning platform that offers a set of HTTP endpoints to control a fleet of ships and explore a multiplayer universe.  The API is documented using [OpenAPI](https://github.com/SpaceTradersAPI/api-docs). You can send your first request right here in your browser to check the status of the game server.  ```json http {   \"method\": \"GET\",   \"url\": \"https://api.spacetraders.io/v2\", } ```  Unlike a traditional game, SpaceTraders does not have a first-party client or app to play the game. Instead, you can use the API to build your own client, write a script to automate your ships, or try an app built by the community.  We have a [Discord channel](https://discord.com/invite/jh6zurdWk5) where you can share your projects, ask questions, and get help from other players.   

    The version of the OpenAPI document: 2.0.0
    Contact: joel@spacetraders.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json



from pydantic import BaseModel, Field, StrictInt, StrictStr, conint, validator

class ShipCrew(BaseModel):
    """
    The ship's crew service and maintain the ship's systems and equipment.  # noqa: E501
    """
    current: StrictInt = Field(default=..., description="The current number of crew members on the ship.")
    required: StrictInt = Field(default=..., description="The minimum number of crew members required to maintain the ship.")
    capacity: StrictInt = Field(default=..., description="The maximum number of crew members the ship can support.")
    rotation: StrictStr = Field(default=..., description="The rotation of crew shifts. A stricter shift improves the ship's performance. A more relaxed shift improves the crew's morale.")
    morale: conint(strict=True, le=100, ge=0) = Field(default=..., description="A rough measure of the crew's morale. A higher morale means the crew is happier and more productive. A lower morale means the ship is more prone to accidents.")
    wages: conint(strict=True, ge=0) = Field(default=..., description="The amount of credits per crew member paid per hour. Wages are paid when a ship docks at a civilized waypoint.")
    __properties = ["current", "required", "capacity", "rotation", "morale", "wages"]

    @validator('rotation')
    def rotation_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('STRICT', 'RELAXED'):
            raise ValueError("must be one of enum values ('STRICT', 'RELAXED')")
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
    def from_json(cls, json_str: str) -> ShipCrew:
        """Create an instance of ShipCrew from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ShipCrew:
        """Create an instance of ShipCrew from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ShipCrew.parse_obj(obj)

        _obj = ShipCrew.parse_obj({
            "current": obj.get("current"),
            "required": obj.get("required"),
            "capacity": obj.get("capacity"),
            "rotation": obj.get("rotation") if obj.get("rotation") is not None else 'STRICT',
            "morale": obj.get("morale"),
            "wages": obj.get("wages")
        })
        return _obj


