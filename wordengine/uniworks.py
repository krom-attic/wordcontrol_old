import ast


def restore_list(value):
    try:
        restored_list = ast.literal_eval(value)  # TODO Fails on spaces with SyntaxError!
    except ValueError as e:  # If not evaluable than it should be a string
        raise e
        restored_list = [value]
    return restored_list