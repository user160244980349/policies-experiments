import re


global_subs = [

    (r"</?\w+/?>", ""),

    (r"[^a-z0-9,.:;\\/\-\n\s\(\)\{\}*?!\[\]]", ""),
    (r"\n+", ""),
    (r"\s+", " "),
    (r"^[\n ]+", ""),

    (r"[\w\-]+@[a-z]+\.[a-z]{2,}", "{removed e-mail}"),
    (r"(https?://)?(www\.)?(([\w\-]+\.)+[a-z]{2,})(/[\w\-]+)*", "{removed hyperref}"),

    (r"^\s{4}", ""),

    (r" ([.,:;!?\)\}\]])", "\g<1>"),
    (r"([.,:;!?\)\}\]])(\w+)", "\g<1> \g<2>"),
    (r"(\w|[\}\]\)])\n", "\g<1>.\n"),
    (r"([\[\(\{]) ", "\g<1>"),
    (r"([\}\]\)])([\{\[\(])", "\g<1> \g<2>"),

    (r"\n{2,}", "\n")
]

global_regexps = [(re.compile(s[0], flags=re.MULTILINE | re.IGNORECASE), s[1]) for s in global_subs]


def clean(text): 

    for r in global_regexps:
        text = r[0].sub(r[1], text)

    return text