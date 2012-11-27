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

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.filter
def objlink(obj):
    """
    Renders an HTML <a> for the given object, using its default unicode
    representation and url as returned by its ``get_absolute_url`` method (if
    any).
    """
    if hasattr(obj, 'get_absolute_url'):
        return mark_safe(u'<a href="%s">%s</a>' % (
                    escape(obj.get_absolute_url()),
                    escape(unicode(obj))))
    else:
        return unicode(obj)

@register.filter
def textlink(text, href):
    """Renders an HTML <a> linking ``text`` to ``href``"""
    return mark_safe(u'<a href="%s">%s</a>' % (escape(href), escape(text)))

