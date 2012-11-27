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
from django.utils.translation import ugettext_lazy as _

from ..models import CAMARA_DISPLAYS_LONG, CAMARA_DISPLAYS_SHORT, \
                     CAMARA_SLUGS, CAMARA_LEGISLADOR_TIPO_DISPLAY_PLURAL, \
                     CAMARA_LEGISLADOR_TIPO_DISPLAY


register = template.Library()


@register.filter
def camara_display_short(camara_slug_or_key):
    displays = CAMARA_DISPLAYS_SHORT
    if camara_slug_or_key in ('S', 'senadores'):
        return displays['S']
    elif camara_slug_or_key in ('D', 'diputados'):
        return displays['D']
    else:
        return u''


@register.filter
def camara_display_long(camara_slug_or_key):
    displays = CAMARA_DISPLAYS_LONG
    if camara_slug_or_key in ('S', 'senadores'):
        return displays['S']
    elif camara_slug_or_key in ('D', 'diputados'):
        return displays['D']
    else:
        return u''


@register.filter
def camara_slug(camara_key):
    return CAMARA_SLUGS.get(camara_key, u'')


@register.filter
def camara_legislador_tipo_display(camara_key):
    return CAMARA_LEGISLADOR_TIPO_DISPLAY.get(camara_key, _(u'Legislador'))


@register.filter
def camara_legislador_tipo_display_plural(camara_key):
    return CAMARA_LEGISLADOR_TIPO_DISPLAY_PLURAL.get(camara_key,
                                                     _(u'Legisladores'))
