# coding: utf-8
#
# MediaSanción, aplicación web para acceder a los datos públicos de la
# actividad legislativa en Argentina.
# Copyright (C) 2010,2011 Renzo Carbonara <renzo @carbonara .com .ar>
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

from ..models import CAMARA_CHOICES_LONG_DISPLAYS, \
                     CAMARA_CHOICES_DISPLAYS, CAMARA_CHOICES_SLUGS


register = template.Library()


@register.filter
def camara_display(camara_slug_or_key):
    displays = CAMARA_CHOICES_DISPLAYS
    if camara_slug_or_key in ('S', 'senadores'):
        return displays['S']
    elif camara_slug_or_key in ('D', 'diputados'):
        return displays['D']
    else:
        return u''


@register.filter
def camara_display_long(camara_slug_or_key):
    displays = CAMARA_CHOICES_LONG_DISPLAYS
    if camara_slug_or_key in ('S', 'senadores'):
        return displays['S']
    elif camara_slug_or_key in ('D', 'diputados'):
        return displays['D']
    else:
        return u''


@register.filter
def camara_slug(camara_key):
    if camara_key in CAMARA_CHOICES_SLUGS:
        return CAMARA_CHOICES_SLUGS[camara_key]
    else:
        return u''
