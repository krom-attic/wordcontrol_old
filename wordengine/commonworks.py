import ast

from wordengine.global_const import *


def restore_list(value):
    if re.match(RE_REST_LIST, value):  # TODO Catches not every incorrect string
        restored_list = ast.literal_eval(value)
    else:
        restored_list = [value]
    return restored_list


def restore_tuple(value):
    if re.match(RE_REST_TUPLE, value):  # TODO Catches not every incorrect string
        restored_tuple = ast.literal_eval(value)
    else:
        restored_tuple = (value, )
    return restored_tuple
