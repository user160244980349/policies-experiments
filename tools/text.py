from re import sub


def remove_quotes(text):
    return sub(r"[\'\"“]", " ", text)


def remove_br(text):
    return sub(r"<br>", "\n", text)


def remove_strong(text):
    return sub(r"<strong>", "", sub(r"</strong>", " ", text))


def remove_ul(text):
    return sub(r"<ul>", "", sub(r"</ul>", " ", text))


def remove_li(text):
    return sub(r"<li>", "", sub(r"</li>", " ", text))


def remove_newlines(text):
    return sub(r"\s*\n+\s*\n*", "\n", text)


def trim(text):
    return sub(r"(\s*\n+\s*)$|^(\s*\n+\s*)", "", text)


def remove_spaces(text):
    return sub(r" {2,}", " ", text)


def remove_digits(text):
    return sub(r"\d+", "", text)


def remove_links(text):
    return sub(r" (.*/)+", "", text)


def remove_spec_chars(text):
    return sub(r"[_|@#$.,;:&`\"\'()]|( - )|(\n +$)", " ", text)
