from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

@register.filter
def split(value, delimiter):
    return value.split(delimiter)

@register.filter
def sumar_columna(lista, indice):
    try:
        return sum(fila[indice] for fila in lista)
    except:
        return 0