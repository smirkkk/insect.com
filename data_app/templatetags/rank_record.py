from django import template
register = template.Library()

@register.filter
def insert_summoner(value, summoner):
    try:
        value = value.replace('[소환사]', summoner.summoner_name)
    except AttributeError:
        pass

    return value
