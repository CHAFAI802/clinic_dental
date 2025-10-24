from django import template

register = template.Library()

@register.filter
def dict_get(dictionnaire, key):
    """
    Récupère la valeur de la clé `key` dans le dictionnaire `dictionnaire`.
    Usage : {{ mydict|dict_get:cle }}
    """
    if not dictionnaire:
        return ''
    return dictionnaire.get(key, '')
