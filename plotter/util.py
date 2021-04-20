## Helper classes and functions

class EvaluationError(Exception):
    pass


def split_str(string, sep=[',']):
    """
    Splits a string based on the list of separators, keeping the seprators.

    Parameters
    ----------
    string : str
        The string to split
    sep : list(str)
        The list of separators. Defaults to [','].
    
    Returns
    -------
    list_ : list(str)
        The list of separated strings and separators.
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