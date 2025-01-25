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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictInt, conlist, constr
from openapi_client.models.shipyard_ship import ShipyardShip
from openapi_client.models.shipyard_ship_types_inner import ShipyardShipTypesInner
from openapi_client.models.shipyard_transaction import ShipyardTransaction

class Shipyard(BaseModel):
    """
      # noqa: E501
    """
    symbol: constr(strict=True, min_length=1) = Field(default=..., description="The symbol of the shipyard. The symbol is the same as the waypoint where the shipyard is located.")
    ship_types: conlist(ShipyardShipTypesInner) = Field(default=..., alias="shipTypes", description="The list of ship types available for purchase at this shipyard.")
    transactions: Optional[conlist(ShipyardTransaction)] = Field(default=None, description="The list of recent transactions at this shipyard.")
    ships: Optional[conlist(ShipyardShip)] = Field(default=None, description="The ships that are currently available for purchase at the shipyard.")
    modifications_fee: StrictInt = Field(default=..., alias="modificationsFee", description="The fee to modify a ship at this shipyard. This includes installing or removing modules and mounts on a ship. In the case of mounts, the fee is a flat rate per mount. In the case of modules, the fee is per slot the module occupies.")
    __properties = ["symbol", "shipTypes", "transactions", "ships", "modificationsFee"]

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
    def from_json(cls, json_str: str) -> Shipyard:
        """Create an instance of Shipyard from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in ship_types (list)
        _items = []
        if self.ship_types:
            for _item in self.ship_types:
                if _item:
                    _items.append(_item.to_dict())
            _dict['shipTypes'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in transactions (list)
        _items = []
        if self.transactions:
            for _item in self.transactions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['transactions'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in ships (list)
        _items = []
        if self.ships:
            for _item in self.ships:
                if _item:
                    _items.append(_item.to_dict())
            _dict['ships'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Shipyard:
        """Create an instance of Shipyard from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Shipyard.parse_obj(obj)

        _obj = Shipyard.parse_obj({
            "symbol": obj.get("symbol"),
            "ship_types": [ShipyardShipTypesInner.from_dict(_item) for _item in obj.get("shipTypes")] if obj.get("shipTypes") is not None else None,
            "transactions": [ShipyardTransaction.from_dict(_item) for _item in obj.get("transactions")] if obj.get("transactions") is not None else None,
            "ships": [ShipyardShip.from_dict(_item) for _item in obj.get("ships")] if obj.get("ships") is not None else None,
            "modifications_fee": obj.get("modificationsFee")
        })
        return _obj


