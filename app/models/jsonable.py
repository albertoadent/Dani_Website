from .db import db
from collections.abc import Iterable


def debug_to_dict(self, rel):
    attrib = getattr(self, rel)
    if isinstance(attrib, Iterable):
        if isinstance(attrib, dict):
            return dict(attrib)
        return [instance.to_dict_basic() for instance in attrib]
    return attrib.to_dict_basic()


def get_attributes(self):
    attributes = list(
        set(
            [
                *[
                    key
                    for key, value in self.__dict__.items()
                    if not callable(value) and "instance" not in key
                ],
                *[
                    key
                    for key in self.__class__.__dict__.keys()
                    if isinstance(getattr(self.__class__, key), property)
                    and not callable(getattr(self, key))
                ],
            ]
        )
    )
    return [*attributes, "created_at_iso", "updated_at_iso"]


def get_attributes_only(self):
    attributes = [
        key for key in get_attributes(self) if key not in get_relationships(self)
    ]
    return attributes


def get_relationships(self):
    relationships = [
        key
        for key in self.__dir__()
        if "_sa_" not in key
        and "__" not in key
        and "registry" not in key
        and key
        not in [
            "query",
            "metadata",
            "query",
            "is_active",
            "is_authenticated",
            "is_anonymous",
        ]
        and not callable(getattr(self, key, None))
        and key in get_attributes(self)
        and (
            isinstance(getattr(self, key), list)
            or isinstance(getattr(self, key), db.Model)
        )
    ]
    return relationships


class JSONable:
    def to_dict_basic(self):
        return {
            key: getattr(self, key)
            for key in get_attributes_only(self)
            if key != "hashed_password"
        }

    def to_dict(self):
        return {
            **self.to_dict_basic(),
            **{rel: debug_to_dict(self, rel) for rel in get_relationships(self)},
        }

    def to_json(self):
        def to_camel_case(string):
            strings = string.split("_")
            return f'{strings[0]}{"".join(sub_string.capitalize() for sub_string in strings[1:])}'

        def convert_keys_to_camel_case(dictionary={}):
            output = {}
            for key in dictionary.keys():
                value = dictionary[key]
                if isinstance(value, dict):
                    value = convert_keys_to_camel_case(value)
                if isinstance(value, list):
                    value = [convert_keys_to_camel_case(item) for item in value]
                output[to_camel_case(key)] = value
            return output

        return convert_keys_to_camel_case(self.to_dict())

    def __repr__(self):
        attribute_string = ",\n".join(
            [
                f"{attribute}: '{getattr(self, attribute)}'"
                for attribute in get_attributes(self)
                if attribute != "id"
                and attribute != "created_at"
                and attribute != "updated_at"
                and attribute != "password"
            ]
        )
        return f"<{type(self).__name__} {str(self.id)}>\n{attribute_string}"
