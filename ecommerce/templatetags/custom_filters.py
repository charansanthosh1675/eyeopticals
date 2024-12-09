from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply two values."""
    return value * arg
