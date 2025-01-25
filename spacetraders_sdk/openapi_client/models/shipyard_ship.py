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
from pydantic import BaseModel, Field, StrictInt, StrictStr, conlist
from openapi_client.models.activity_level import ActivityLevel
from openapi_client.models.ship_engine import ShipEngine
from openapi_client.models.ship_frame import ShipFrame
from openapi_client.models.ship_module import ShipModule
from openapi_client.models.ship_mount import ShipMount
from openapi_client.models.ship_reactor import ShipReactor
from openapi_client.models.ship_type import ShipType
from openapi_client.models.shipyard_ship_crew import ShipyardShipCrew
from openapi_client.models.supply_level import SupplyLevel

class ShipyardShip(BaseModel):
    """
      # noqa: E501
    """
    type: ShipType = Field(...)
    name: StrictStr = Field(...)
    description: StrictStr = Field(...)
    supply: SupplyLevel = Field(...)
    activity: Optional[ActivityLevel] = None
    purchase_price: StrictInt = Field(default=..., alias="purchasePrice")
    frame: ShipFrame = Field(...)
    reactor: ShipReactor = Field(...)
    engine: ShipEngine = Field(...)
    modules: conlist(ShipModule) = Field(...)
    mounts: conlist(ShipMount) = Field(...)
    crew: ShipyardShipCrew = Field(...)
    __properties = ["type", "name", "description", "supply", "activity", "purchasePrice", "frame", "reactor", "engine", "modules", "mounts", "crew"]

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
    def from_json(cls, json_str: str) -> ShipyardShip:
        """Create an instance of ShipyardShip from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of frame
        if self.frame:
            _dict['frame'] = self.frame.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reactor
        if self.reactor:
            _dict['reactor'] = self.reactor.to_dict()
        # override the default output from pydantic by calling `to_dict()` of engine
        if self.engine:
            _dict['engine'] = self.engine.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in modules (list)
        _items = []
        if self.modules:
            for _item in self.modules:
                if _item:
                    _items.append(_item.to_dict())
            _dict['modules'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in mounts (list)
        _items = []
        if self.mounts:
            for _item in self.mounts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['mounts'] = _items
        # override the default output from pydantic by calling `to_dict()` of crew
        if self.crew:
            _dict['crew'] = self.crew.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ShipyardShip:
        """Create an instance of ShipyardShip from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ShipyardShip.parse_obj(obj)

        _obj = ShipyardShip.parse_obj({
            "type": obj.get("type"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "supply": obj.get("supply"),
            "activity": obj.get("activity"),
            "purchase_price": obj.get("purchasePrice"),
            "frame": ShipFrame.from_dict(obj.get("frame")) if obj.get("frame") is not None else None,
            "reactor": ShipReactor.from_dict(obj.get("reactor")) if obj.get("reactor") is not None else None,
            "engine": ShipEngine.from_dict(obj.get("engine")) if obj.get("engine") is not None else None,
            "modules": [ShipModule.from_dict(_item) for _item in obj.get("modules")] if obj.get("modules") is not None else None,
            "mounts": [ShipMount.from_dict(_item) for _item in obj.get("mounts")] if obj.get("mounts") is not None else None,
            "crew": ShipyardShipCrew.from_dict(obj.get("crew")) if obj.get("crew") is not None else None
        })
        return _obj


