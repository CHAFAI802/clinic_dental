# documents/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Ajoute une classe CSS à un champ de formulaire.
    Usage : {{ form.field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css_class})


@register.filter(name='placeholder')
def placeholder(field, text):
    """
    Ajoute un placeholder au champ de formulaire.
    Usage : {{ form.field|placeholder:"Nom du patient" }}
    """
    return field.as_widget(attrs={"placeholder": text})


@register.filter(name='add_attr')
def add_attr(field, arg):
    """
    Ajoute n’importe quel attribut personnalisé à un champ.
    Exemple : {{ form.field|add_attr:"rows=5" }}
    """
    attr, value = arg.split('=')
    return field.as_widget(attrs={attr: value})
