# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template, forms

from awesome_avatar.widgets import AvatarWidget

register = template.Library()


def form_grid_specs(specs):
    if not specs:
        return None
    label_sizes, control_sizes, offset_sizes = [], [], []
    for spec in specs.split(','):
        label_sizes.append('col-{0}'.format(spec))
        size, col = spec.split('-')
        offset_sizes.append('col-{0}-offset-{1}'.format(size, col))
        col = 12 - int(col)
        control_sizes.append('col-{0}-{1}'.format(size, col))
    return {
        'label': ' '.join(label_sizes),
        'control': ' '.join(control_sizes),
        'offset': ' '.join(offset_sizes),
    }


@register.inclusion_tag('bootstrap/input.html')
def input(field, label=None, disabled=False, type=None, sizes='md-4,lg-3'):
    return {
        'field': field,
        'label': label or field.label,
        'value': field.value() or (field.initial if hasattr(field, 'initial') else ''),
        'disabled': disabled,
        'type': type or field.field.widget.input_type or 'text',
        'sizes': form_grid_specs(sizes),
    }


@register.inclusion_tag('bootstrap/checkbox.html')
def checkbox(field, label=None, disabled=False, sizes='md-4,lg-3'):
    return {
        'field': field,
        'label': label or field.label,
        'checked': len(field.value() or (field.initial if hasattr(field, 'initial') else '')) > 0,
        'disabled': disabled,
        'sizes': form_grid_specs(sizes),
    }


@register.inclusion_tag('bootstrap/textarea.html')
def textarea(field, label=None, disabled=False, rows=None, sizes='md-4,lg-3'):
    rows = rows or field.field.widget.attrs.get('rows', 3)
    return {
        'field': field,
        'label': label or field.label,
        'value': field.value() or (field.initial if hasattr(field, 'initial') else ''),
        'disabled': disabled,
        'sizes': form_grid_specs(sizes),
        'rows': rows
    }


@register.inclusion_tag('bootstrap/field.html')
def form_field(field, *args, **kwargs):
    data = {}
    if isinstance(field.field.widget, forms.CheckboxInput):
        data['widget'] = 'checkbox'
        data.update(checkbox(field, *args, **kwargs))
    elif isinstance(field.field.widget, forms.Textarea):
        data['widget'] = 'textarea'
        data.update(textarea(field, *args, **kwargs))
    elif isinstance(field.field.widget, forms.TextInput):
        data['widget'] = 'input'
        data.update(input(field, *args, **kwargs))
    else:
        data['field'] = field
    return data
