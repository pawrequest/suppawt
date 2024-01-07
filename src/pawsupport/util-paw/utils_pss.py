import os


def param_or_env(env_key: str, value: str | None, none_is_false=False) -> str | bool:
    value = value or os.environ.get(env_key)
    if value is None:
        if none_is_false:
            return False
        raise ValueError(f"{env_key} was not provided and is not an environment variable")

    return value


def printel(*els):  # elementtree elements
    print("printel")
    if isinstance(els, str):
        els = [els]
    for el in els:
        print(el)
        for elem in el.iter():
            print(elem.tag, elem.text)


def toPascal(x):  # LikeThis
    x = x.title()
    for y in x:
        if not y.isalpha():
            if not y.isnumeric():
                x = x.replace(y, "")
    s = x.split()
    print("JOIN", "".join(i.capitalize() for i in s[1:]))
    return "".join(i.capitalize() for i in s[1:])


def toCamel(x):  # likeThis
    for i in str(x):
        if not i.isalnum():
            x = x.replace(i, " ")
    s = x.lower().split()
    return s[0] + "".join(i.capitalize() for i in s[1:])


def withoutKeys(d, keys):
    ...
    return {x: d[x] for x in d if x not in keys}


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
