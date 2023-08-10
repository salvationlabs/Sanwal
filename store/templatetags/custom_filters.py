from django import template

register = template.Library()

@register.filter
def group_attributes(attributes):
    attribute_dict = {}
    result = []

    for attribute in attributes:
        a_v = f'<button class="btn btn-sm basket">{attribute.value}</button>'
        if attribute.specification.name in attribute_dict:
            attribute_dict[attribute.specification.name].append(a_v)
        else:
            attribute_dict[attribute.specification.name] = [a_v]

    for key, values in attribute_dict.items():
        result.append(f"{key}: {' '.join(values)}")

    return '<br/> <br/>'.join(result)
