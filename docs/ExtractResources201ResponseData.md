# ExtractResources201ResponseData


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cooldown** | [**Cooldown**](Cooldown.md) |  | 
**extraction** | [**Extraction**](Extraction.md) |  | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**events** | [**List[ExtractResources201ResponseDataEventsInner]**](ExtractResources201ResponseDataEventsInner.md) |  | 

## Example

```python
from openapi_client.models.extract_resources201_response_data import ExtractResources201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractResources201ResponseData from a JSON string
extract_resources201_response_data_instance = ExtractResources201ResponseData.from_json(json)
# print the JSON string representation of the object
print ExtractResources201ResponseData.to_json()

# convert the object into a dict
extract_resources201_response_data_dict = extract_resources201_response_data_instance.to_dict()
# create an instance of ExtractResources201ResponseData from a dict
extract_resources201_response_data_from_dict = ExtractResources201ResponseData.from_dict(extract_resources201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


