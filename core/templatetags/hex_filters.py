from django import template

register = template.Library()

@register.filter
def hex_to_rgb(value):
    """
    Convertit un code couleur hexadécimal #RRGGBB en 'R,G,B' (string)
    Usage dans template: {{ '#FF00AA'|hex_to_rgb }} => '255,0,170'
    """
    if not value:
        return "0,0,0"
    value = value.strip()
    if value.startswith("#"):
        value = value[1:]
    if len(value) == 3:  # format #RGB
        value = "".join([c*2 for c in value])
    try:
        r = int(value[0:2], 16)
        g = int(value[2:4], 16)
        b = int(value[4:6], 16)
        return f"{r},{g},{b}"
    except Exception:
        return "0,0,0"
