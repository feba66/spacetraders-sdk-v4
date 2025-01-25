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


from typing import List
from pydantic import BaseModel, Field, conlist
from openapi_client.models.cooldown import Cooldown
from openapi_client.models.ship_cargo import ShipCargo
from openapi_client.models.ship_refine201_response_data_produced_inner import ShipRefine201ResponseDataProducedInner

class ShipRefine201ResponseData(BaseModel):
    """
    ShipRefine201ResponseData
    """
    cargo: ShipCargo = Field(...)
    cooldown: Cooldown = Field(...)
    produced: conlist(ShipRefine201ResponseDataProducedInner) = Field(default=..., description="Goods that were produced by this refining process.")
    consumed: conlist(ShipRefine201ResponseDataProducedInner) = Field(default=..., description="Goods that were consumed during this refining process.")
    __properties = ["cargo", "cooldown", "produced", "consumed"]

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
    def from_json(cls, json_str: str) -> ShipRefine201ResponseData:
        """Create an instance of ShipRefine201ResponseData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of cargo
        if self.cargo:
            _dict['cargo'] = self.cargo.to_dict()
        # override the default output from pydantic by calling `to_dict()` of cooldown
        if self.cooldown:
            _dict['cooldown'] = self.cooldown.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in produced (list)
        _items = []
        if self.produced:
            for _item in self.produced:
                if _item:
                    _items.append(_item.to_dict())
            _dict['produced'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in consumed (list)
        _items = []
        if self.consumed:
            for _item in self.consumed:
                if _item:
                    _items.append(_item.to_dict())
            _dict['consumed'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ShipRefine201ResponseData:
        """Create an instance of ShipRefine201ResponseData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ShipRefine201ResponseData.parse_obj(obj)

        _obj = ShipRefine201ResponseData.parse_obj({
            "cargo": ShipCargo.from_dict(obj.get("cargo")) if obj.get("cargo") is not None else None,
            "cooldown": Cooldown.from_dict(obj.get("cooldown")) if obj.get("cooldown") is not None else None,
            "produced": [ShipRefine201ResponseDataProducedInner.from_dict(_item) for _item in obj.get("produced")] if obj.get("produced") is not None else None,
            "consumed": [ShipRefine201ResponseDataProducedInner.from_dict(_item) for _item in obj.get("consumed")] if obj.get("consumed") is not None else None
        })
        return _obj


