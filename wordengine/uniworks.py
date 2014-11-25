import ast


def restore_list(value):
    restored_list = ast.literal_eval(value)  # TODO Fails on spaces with SyntaxError!
    # try:
    #     restored_list = ast.literal_eval(value)
    # except ValueError as e:  # If not evaluable than it should be a string
    #     restored_list = [value]
    return restored_list