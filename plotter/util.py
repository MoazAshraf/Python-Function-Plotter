## Helper classes and functions

class EvaluationError(Exception):
    pass


def split_str(string, sep=[',']):
    """
    Splits a string based on the list of separators, keeping the seprators
    """

    list_ = []

    s = ""
    for c in string:
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