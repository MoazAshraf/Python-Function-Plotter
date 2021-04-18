## Helper functions

def split_str(string, sep=[',']):
    """
    Splits a string based on the list of separators, keeping the seprators
    and ignoring whitespace
    """

    list_ = []

    s = ""
    for c in string:
        if c.isspace():
            continue
        if c in sep:
            if s:
                list_.append(s)
            list_.append(c)
            s = ""
        else:
            s += c
    if s:
        list_.append(s)

    return list_