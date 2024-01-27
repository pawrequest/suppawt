import re


def obj_to_dict(obj: object):
    serializable_types = (int, float, str, bool, type(None))
    return {k: v for k, v in vars(obj).items() if isinstance(v, serializable_types)}


def to_camel(x):
    words = x.split()
    return "".join([words[0].lower()] + [word.capitalize() for word in words[1:]])


def without_keys(d, keys):
    ...
    return {x: d[x] for x in d if x not in keys}


def to_snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
