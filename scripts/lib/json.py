import datetime
import json


def obj_from_json(json_dict):
    for key, value in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict


def obj_to_json(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f'don\'t know how to turn {type(obj)} to json!')


def load_json(string):
    return json.loads(string, object_hook=obj_from_json)


def dump_json(obj):
    return json.dumps(obj, default=obj_to_json, sort_keys=True)
