from django import template

register=template.Library()

@register.filter(name='get_temp_name')
def get_temp_name(value):
    name,extra=value.split('@')
    return name