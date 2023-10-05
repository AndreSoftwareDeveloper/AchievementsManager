from itertools import zip_longest
from django import template

register = template.Library()


@register.filter
def zip_longest_filter(list1, list2):
    return zip_longest(list1, list2)
