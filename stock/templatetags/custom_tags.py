from django import template

register = template.Library()

@register.filter
def dict_get(dictionnaire, key):
    """
    Récupère la valeur de la clé `key` dans le dictionnaire `dictionnaire`.
    Usage dans template : {{ mydict|dict_get:cle }}
    """
    if dictionnaire is None:
        return ''
    try:
        return dictionnaire.get(key, '')
    except Exception:
        return ''
