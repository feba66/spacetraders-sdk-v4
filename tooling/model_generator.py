import json
import os
from pydantic import BaseModel

from util import conv_camel_to_snake, conv_property_type

models_path = "api-docs/models"
output_path = "tmp/own_gen/models"


def add_description(indent, description, title=False):
    if description:
        suffix = "" if len(description) < 80 else "  # noqa: E501"
        indent_str = " " * (4 * indent)
        if not title:
            return f'{indent_str}""" {description.strip()} """{suffix}\n'
        else:
            return f'{indent_str}"""\n{indent_str}{description.strip()}\n{indent_str}"""{suffix}\n\n'
    return ""


def get_property_type(property_data):
    imports = []
    property_type = conv_property_type(property_data["type"])
    if property_type == "list":
        if "items" in property_data:
            if "type" in property_data["items"]:
                property_type = f"list[{conv_property_type(property_data['items']['type'])}]"
            else:
                imported_type = property_data["items"]["$ref"].split(".")[1].replace("/", "")
                imports.append(imported_type)
                property_type = f"list[{imported_type}]  # TODO: {property_data['items']}"
    return property_type, imports


for file in os.listdir(models_path):
    with open(f"{models_path}/{file}", "rb") as f:
        data = json.load(f)
    if "deprecated" in data and data["deprecated"]:
        continue
    string = None
    typ = data["type"] if "type" in data else None
    description = data["description"] if "description" in data else None
    subfolder = ""
    if typ and typ == "string":

        enum = data["enum"] if "enum" in data else None
        enum_descriptions = data["x-enumDescriptions"] if "x-enumDescriptions" in data else None
        default = data["default"] if "default" in data else None

        if enum:
            # subfolder = "/enums"
            string = "from __future__ import annotations\nfrom enum import Enum\nimport json\n\n\n"
            string += f"class {file.split('.')[0]}(Enum):\n"
            string += add_description(1, description, title=True)
            for i, e in enumerate(enum):
                string += f'    {e.upper()} = "{e}"\n'

                if enum_descriptions:
                    string += add_description(1, enum_descriptions[e])

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
            if property_name in ["yield"]:
                property_name = f"{property_name}_"
            if "type" in property_data:
                optional = "\n"
                if "required" in data and property_name not in data["required"]:
                    optional = " | None\n"

                property_type, imports = get_property_type(property_data)
                for imp in imports:
                    if not f"import {imp}" in string:
                        string = string.replace("BaseModel\n", f"BaseModel\nfrom .{imp} import {imp}\n")
                string += f"    {conv_camel_to_snake(property_name)}: {property_type}{optional}"

                if "description" in property_data:
                    string += add_description(1, property_data["description"])

            else:
                imported_type = property_data["$ref"].split(".")[1].replace("/", "")
                if not f"import {imported_type}" in string:
                    string = string.replace("BaseModel\n", f"BaseModel\nfrom .{imported_type} import {imported_type}\n")
                string += f"    {conv_camel_to_snake(property_name)}: {imported_type}"
                string += f"  # TODO: {property_data}\n"
                # string += f"    # TODO: {conv_camel_to_snake(property_name)}: {property_data}\n"

    else:
        pass
    if string and string != "":
        with open(f"{output_path}{subfolder}/{file.split('.')[0]}.py", "w") as f:
            f.write(string)

print()
