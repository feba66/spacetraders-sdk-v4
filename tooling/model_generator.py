import json
import os
from pydantic import BaseModel

from util import conv_camel_to_snake, conv_property_type

models_path = "api-docs/models"
output_path = "tmp/own_gen/models"
keys = []
for file in os.listdir(models_path):
    with open(f"{models_path}/{file}", "rb") as f:
        data = json.load(f)

    string = None
    typ = data["type"] if "type" in data else None
    description = data["description"] if "description" in data else None
    subfolder = ""
    if typ and typ == "string":

        enum = data["enum"] if "enum" in data else None
        enum_descriptions = data["x-enumDescriptions"] if "x-enumDescriptions" in data else None
        default = data["default"] if "default" in data else None

        if enum:
            subfolder = "/enums"
            string = "from __future__ import annotations\nfrom enum import Enum\nimport json\n\n\n"
            string += f"class {file.split('.')[0]}(Enum):\n"
            string += f'    """\n    {description}\n    """\n\n'
            for i, e in enumerate(enum):
                string += f'    {e.upper()} = "{e}"\n'
                if enum_descriptions:
                    string += f'    """ {enum_descriptions[e]}"""\n'
            # @classmethod
            # def from_json(cls, json_str: str) -> ActivityLevel:
            #     """Create an instance of ActivityLevel from a JSON string"""
            #     return ActivityLevel(json.loads(json_str))
            string += f"\n    @classmethod\n    def from_json(cls, json_str: str) -> {file.split('.')[0]}:\n"
            string += f'        """Create an instance of {file.split('.')[0]} from a JSON string"""\n'
            string += f"        return {file.split('.')[0]}(json.loads(json_str))\n"

        else:
            pass  # Systen and waypoint symbols
        print(file)
    elif typ and typ == "object":
        string = "import json\nfrom pydantic import BaseModel\n\n\n"
        string += f"class {file.split('.')[0]}(BaseModel):\n"
        string += f'    """\n    {description}\n    """\n\n'

        for property_name, property_data in data["properties"].items():
            if "type" in property_data:
                optional = "\n"
                if "required" in data and property_name not in data["required"]:
                    optional = " | None\n"

                string += f'    {conv_camel_to_snake(property_name)}: {conv_property_type(property_data["type"])}{optional}'
                if "description" in property_data:
                    need_ignore = "" if len(property_data["description"]) < 80 else "  # noqa: E501"
                    string += f'    """{property_data["description"]}"""{need_ignore}\n'
                else:
                    string += ""

            else:
                string += f"    # TODO: {conv_camel_to_snake(property_name)}: {property_data}\n"

        for k in data.keys():
            if k not in keys:
                keys.append(k)
    else:
        pass
    if string and string != "":
        with open(f"{output_path}{subfolder}/{file.split('.')[0]}.py", "w") as f:
            f.write(string)

print(keys)
