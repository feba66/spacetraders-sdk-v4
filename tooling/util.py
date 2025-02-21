import re


def conv_camel_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def conv_property_type(typ):
    if typ == "string":
        return "str"
    if typ == "integer":
        return "int"
    if typ == "boolean":
        return "bool"
    if typ == "array":
        return "list"
    return typ
