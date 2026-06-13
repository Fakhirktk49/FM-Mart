from django import template

register=template.Library()

@register.filter(name='get_temp_name')
def get_temp_name(value):
    if '@' in value:
        name,extra=value.split('@')
        return name
    else:
        return value