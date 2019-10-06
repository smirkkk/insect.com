from django import template
register = template.Library()

@register.filter
def insert_summoner(value, summoner):
    try:
        value = value.replace('[소환사]', '<span class="review_summoner">' + summoner.summoner_name + '</span>')
    except AttributeError:
        pass

    return value
