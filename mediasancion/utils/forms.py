# coding: utf-8
#
# MediaSanción, aplicación web para acceder a los datos públicos de la
# actividad legislativa en Argentina.
# Copyright (C) 2010,2011,2012 Renzo Carbonara <renzo @carbonara .com .ar>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import uuid
from itertools import groupby

from django import forms
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


__all__ = 'UUIDField', 'MultipleUUIDField', 'ModelLookupMultipleChoiceField',


class UUIDField(forms.CharField):
    default_error_messages = {
        'invalid_uuid': _(u'%(value)s is not a valid UUID. %(info)s')
    }

    def to_python(self, value):
        if value in forms.fields.EMPTY_VALUES:
            return None
        try:
            return unicode(uuid.UUID(value))
        except (ValueError, TypeError), e:
            msg = self.error_messages['invalid_uuid'] % { 'value': value, 'info': smart_unicode(e) }
            raise forms.ValidationError(msg)


class MultipleUUIDField(forms.Field):
    widget = forms.SelectMultiple
    hidden_widget = forms.MultipleHiddenInput
    default_error_messages = {
        'invalid_list': _(u'Enter a list of values.'),
        'invalid_uuid': _(u'%(value)s is not a valid UUID. %(info)s')
    }

    def to_python(self, value):
        if value in forms.fields.EMPTY_VALUES:
            return []
        elif not isinstance(value, (list, tuple, set)):
            raise forms.ValidationError(self.error_messages['invalid_list'])
        out = set()
        for val in value:
            try:
                out.add(smart_unicode(uuid.UUID(val)))
            except (ValueError, TypeError), e:
                print self.error_messages
                msg = self.error_messages['invalid_uuid'] % { 'value': val, 'info': smart_unicode(e) }
                raise forms.ValidationError(msg)
        return out


class ModelLookupMultipleChoiceField(forms.ModelChoiceField):
    """
    A ModelChoiceField whose choices are a model QuerySet.

    By default, model object lookup is done by matching the primary key field
    value. You can change that through the ``to_field_name`` attribute.
    """
    widget = forms.SelectMultiple
    hidden_widget = forms.MultipleHiddenInput
    default_error_messages = {
        'invalid_list': _(u'Enter a list of values.'),
        'invalid_choice': _(u'Select a valid choice. %s is not one of the'
                            u' available choices.'),
        'too_many_results': _(u'Too many results for %s'),
    }

    def __init__(self, queryset, cache_choices=False, required=True,
                 widget=None, label=None, initial=None, help_text=None,
                 to_field_name=None, *args, **kwargs):
        super(ModelLookupMultipleChoiceField, self).__init__(queryset, None,
            cache_choices, required, widget, label, initial, help_text,
            to_field_name, *args, **kwargs)
        self.to_field_name = to_field_name or 'pk'

    def to_python(self, value):
        if value in forms.fields.EMPTY_VALUES:
            return []
        if not isinstance(value, (list, tuple, set)):
            raise forms.ValidationError(self.error_messages['invalid_list'])
        if not isinstance(value, set):
            value = set(value)

        qs = self.queryset.filter(**{'%s__in' % self.to_field_name: value})

        # Cheap validation follows (so that we query the DB only once)
        dgqs = dict((k, len(tuple(v))) for (k,v) in groupby(qs, lambda x: getattr(x, self.to_field_name)))

        # Check if any of the objects we asked for does not exist.
        for val in value:
            if val not in dgqs:
                raise forms.ValidationError(self.error_messages['invalid_choice'] % val)

        # Check if we got multiple results for the very same key
        for k,v in dgqs.iteritems():
            if v > 1:
                raise forms.ValidationError(self.error_messages['too_many_results'] % k)

        # Everything is OK, we have one object per asked value.
        return qs

