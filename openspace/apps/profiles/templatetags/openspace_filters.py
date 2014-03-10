from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def featureQuery(value, query):
    start = value.lower().index(query)
    if start != 0:
        return '. . . ' + value[start:-1]
    else:
        return value[start:-1]