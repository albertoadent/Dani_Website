class JSONable:
    def relationships(self):
        return [
            key
            for key in self.__dir__()
            if "_sa_" not in key
            and "__" not in key
            and "registry" not in key
            and key not in ["query", "metadata", "query"]
            and not callable(getattr(self, key, None))
            and key not in self.attributes()
        ]

    def attributes(self):
        return list(
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

    def to_dict_basic(self):
        return {
            key: getattr(self, key)
            for key in self.attributes()
            if key != "hashed_password"
        }

    def to_dict(self):
        return {
            **self.to_dict_basic(),
            **{rel: rel.to_dict_basic() for rel in self.relationships()},
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
                output[to_camel_case(key)] = value
            return output

        return convert_keys_to_camel_case(self.to_dict())

    def __repr__(self):
        attribute_string = ",\n".join(
            [
                f"{attribute}: '{getattr(self, attribute)}'"
                for attribute in self.attributes()
                if attribute != "id"
                and attribute != "created_at"
                and attribute != "updated_at"
                and attribute != "password"
            ]
        )
        return f"<{type(self).__name__} {str(self.id)}>\n{attribute_string}"
