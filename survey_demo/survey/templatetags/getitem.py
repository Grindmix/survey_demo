from django import template
register = template.Library()

@register.filter
def index(list, i):
    return list[i]


@register.filter
def get_item(dict, key):
    return dict.get(key)