from datetime import datetime


def validate(data_dict, data, optional=[]):
    errors = {}
    if datetime in data_dict.values():
        format_dates(data)
    for key, val in data_dict.items():
        try:
            if not isinstance(data[key], val):
                errors[key] = (
                    f"{key} is supposed to be of type {val.__name__} but received type {type(data[key]).__name__} instead"
                )
        except KeyError:
            if key in optional:
                continue
            errors[key] = f"{key} is required"
    if len(errors):
        return {"message": "Bad Data", "errors": errors}
    return None


def error_404(obj):
    if not obj:
        return {"message": "Resource not found"}, 404
    return None


def format_dates(obj):
    for key in obj.keys():
        if "date" in key or "Date" in key:
            obj[key] = datetime.fromisoformat(obj[key])


def keys_to_snake(obj):
    def string_to_snake(string):
        string_arr = list(string)
        for i in range(len(string_arr)):
            if string_arr[i].upper() == string_arr[i]:
                string_arr[i] = "_" + string_arr[i].lower()
        return "".join(string_arr)

    return {string_to_snake(key): obj[key] for key in obj.keys()}
