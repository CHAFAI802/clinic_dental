from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """Ajoute une ou plusieurs classes CSS sans écraser celles existantes."""
    existing_classes = field.field.widget.attrs.get("class", "")
    new_classes = f"{existing_classes} {css}".strip()
    return field.as_widget(attrs={"class": new_classes})
