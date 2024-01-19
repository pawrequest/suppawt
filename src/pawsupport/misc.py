import hashlib
import re


def printel(*els):  # elementtree elements
    print("printel")
    if isinstance(els, str):
        els = [els]
    for el in els:
        print(el)
        for elem in el.iter():
            print(elem.tag, elem.text)


def to_camel(x):
    words = x.split()
    return ''.join([words[0].lower()] + [word.capitalize() for word in words[1:]])


def without_keys(d, keys):
    ...
    return {x: d[x] for x in d if x not in keys}


def to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def title_from_snake(s):
    s = s.replace("_", " ")
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s).title()

def snake_name(obj) -> str:
    return to_snake(obj.__name__).lower()


def snake_name_s(obj) -> str:
    return f'{to_snake(obj.__name__).lower()}s'


def unsanitise(string):
    string = (
        string.replace("&amp;", chr(38))
        .replace("&quot;", chr(34))
        .replace("&apos;", chr(39))
        .replace("&lt;", chr(60))
        .replace("&gt;", chr(62))
        .replace("&gt;", chr(32))
        .replace("&#", "")
        .replace(";", "")
        .replace(",", "")
    )
    return string


def get_hash(obj: object):
    mapped = []
    if hasattr(obj, "get_hash"):
        if callable(obj.get_hash):
            return obj.get_hash()
        return obj.get_hash

    if hasattr(obj, "reddit_id"):
        mapped.append(obj.reddit_id)

    if hasattr(obj, "date"):
        mapped.append(str(obj.date))

    if hasattr(obj, "title"):
        mapped.append(obj.title)
    if hasattr(obj, "name"):
        mapped.append(obj.name)

    if not mapped:
        raise ValueError(f"Can't find any hashable attributes on {obj}")
    return hash_simple_md5(mapped)


def hash_simple_md5(data: list):
    return hashlib.md5(",".join(data).encode()).hexdigest()
