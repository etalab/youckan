# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template, forms
from django.template.defaultfilters import stringfilter
from django.utils.text import Truncator
from django.utils.html import escape, strip_tags
from django.utils.safestring import mark_safe
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


@register.inclusion_tag('bootstrap/avatar.html')
def avatar_widget(field, label=None, disabled=False, sizes='md-4,lg-3'):
    return {
        'field': field,
        'label': label or field.label,
        'disabled': disabled,
        'sizes': form_grid_specs(sizes),
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
    elif isinstance(field.field.widget, AvatarWidget):
        data['widget'] = 'avatar'
        data.update(avatar_widget(field, *args, **kwargs))
    else:
        data['field'] = field
    return data


@register.filter(is_safe=True)
@stringfilter
def tooltip_ellipsis(source, length=0):
    ''' return the plain text representation of markdown encoded text.  That
    is the texted without any html tags.  If ``length`` is 0 then it
    will not be truncated.'''
    try:
        length = int(length)
    except ValueError:  # invalid literal for int()
        return source  # Fail silently.
    ellipsis = '<a href rel="tooltip" title="{0}">...</a>'.format(source)
    truncated = Truncator(source).chars(length + 2, truncate='{...}')
    return mark_safe(truncated.replace('{...}', ellipsis))


@register.filter(is_safe=True)
@stringfilter
def popover_ellipsis(source, length=0):
    ''' return the plain text representation of markdown encoded text.  That
    is the texted without any html tags.  If ``length`` is 0 then it
    will not be truncated.'''
    try:
        length = int(length)
    except ValueError:  # invalid literal for int()
        return source  # Fail silently.
    ellipsis = ('<a href rel="popover" data-content="{0}" '
        'data-trigger="hover" data-container="body">...</a>').format(escape(source))
    truncated = Truncator(strip_tags(source)).chars(length)
    nb_words = len(truncated.split(' '))
    html_truncated = Truncator(source).words(nb_words, html=True, truncate='{...}')
    return mark_safe(html_truncated.replace('{...}', ellipsis))
