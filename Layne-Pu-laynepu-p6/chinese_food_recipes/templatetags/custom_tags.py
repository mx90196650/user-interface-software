from django import template

register = template.Library()

@register.filter(name='custom_naturaltime')
def custom_naturaltime(str):
    return str[:-4].split(',')[0] + " ago"