from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Применение декораторов"""
    return field.as_widget(attrs={'class': css})
