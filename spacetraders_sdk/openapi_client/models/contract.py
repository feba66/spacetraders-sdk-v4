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

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, constr, validator
from openapi_client.models.contract_terms import ContractTerms

class Contract(BaseModel):
    """
    Contract details.  # noqa: E501
    """
    id: constr(strict=True, min_length=1) = Field(default=..., description="ID of the contract.")
    faction_symbol: constr(strict=True, min_length=1) = Field(default=..., alias="factionSymbol", description="The symbol of the faction that this contract is for.")
    type: StrictStr = Field(default=..., description="Type of contract.")
    terms: ContractTerms = Field(...)
    accepted: StrictBool = Field(default=..., description="Whether the contract has been accepted by the agent")
    fulfilled: StrictBool = Field(default=..., description="Whether the contract has been fulfilled")
    expiration: datetime = Field(default=..., description="Deprecated in favor of deadlineToAccept")
    deadline_to_accept: Optional[datetime] = Field(default=None, alias="deadlineToAccept", description="The time at which the contract is no longer available to be accepted")
    __properties = ["id", "factionSymbol", "type", "terms", "accepted", "fulfilled", "expiration", "deadlineToAccept"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('PROCUREMENT', 'TRANSPORT', 'SHUTTLE'):
            raise ValueError("must be one of enum values ('PROCUREMENT', 'TRANSPORT', 'SHUTTLE')")
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
    def from_json(cls, json_str: str) -> Contract:
        """Create an instance of Contract from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of terms
        if self.terms:
            _dict['terms'] = self.terms.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Contract:
        """Create an instance of Contract from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Contract.parse_obj(obj)

        _obj = Contract.parse_obj({
            "id": obj.get("id"),
            "faction_symbol": obj.get("factionSymbol"),
            "type": obj.get("type"),
            "terms": ContractTerms.from_dict(obj.get("terms")) if obj.get("terms") is not None else None,
            "accepted": obj.get("accepted") if obj.get("accepted") is not None else False,
            "fulfilled": obj.get("fulfilled") if obj.get("fulfilled") is not None else False,
            "expiration": obj.get("expiration"),
            "deadline_to_accept": obj.get("deadlineToAccept")
        })
        return _obj


