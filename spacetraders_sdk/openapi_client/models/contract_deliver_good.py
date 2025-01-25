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


from pydantic import BaseModel, Field, StrictInt, constr


class ContractDeliverGood(BaseModel):
    """
    The details of a delivery contract. Includes the type of good, units needed, and the destination.  # noqa: E501
    """

    trade_symbol: constr(strict=True, min_length=1) = Field(
        default=..., alias="tradeSymbol", description="The symbol of the trade good to deliver."
    )
    destination_symbol: constr(strict=True, min_length=1) = Field(
        default=..., alias="destinationSymbol", description="The destination where goods need to be delivered."
    )
    units_required: StrictInt = Field(
        default=..., alias="unitsRequired", description="The number of units that need to be delivered on this contract."
    )
    units_fulfilled: StrictInt = Field(
        default=..., alias="unitsFulfilled", description="The number of units fulfilled on this contract."
    )
    __properties = ["tradeSymbol", "destinationSymbol", "unitsRequired", "unitsFulfilled"]

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
    def from_json(cls, json_str: str) -> ContractDeliverGood:
        """Create an instance of ContractDeliverGood from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ContractDeliverGood:
        """Create an instance of ContractDeliverGood from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ContractDeliverGood.parse_obj(obj)

        _obj = ContractDeliverGood.parse_obj(
            {
                "trade_symbol": obj.get("tradeSymbol"),
                "destination_symbol": obj.get("destinationSymbol"),
                "units_required": obj.get("unitsRequired"),
                "units_fulfilled": obj.get("unitsFulfilled"),
            }
        )
        return _obj
