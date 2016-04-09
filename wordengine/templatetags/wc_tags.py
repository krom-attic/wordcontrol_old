from django import template

register = template.Library()


@register.filter
def surround(value, arg):
    """
    Surrounds the value with an arg
    :arg: must be in format "BEGIN:END"
    """
    if value:
        surrounding = arg.split(':', 1)
        if issubclass(type(value), str):
            return value.join(surrounding)
        elif type(value) == list:
            return [v.join(surrounding) for v in value]
        else:
            raise Exception('Unexpected type {}'.format(type(value)))
    else:
        return ''
