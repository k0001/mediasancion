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

from datetime import date
from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

def _base_page_data(page):
    c = {}
    if page.has_previous():
        c['has_other_pages'] = True
        c['has_previous'] = True
        c['previous_page_number'] = page.previous_page_number()
    else:
        c['has_previous'] = False

    if page.has_next():
        c['has_other_pages'] = True
        c['has_next'] = True
        c['next_page_number'] = page.next_page_number()
    else:
        c['has_next'] = False

    return c

@register.inclusion_tag('utils/pagination.html')
def show_pagination(page, reverse=False):
    c = _base_page_data(page)
    if reverse:
        c['previous_page_text'] = _(u"next")
        c['next_page_text'] = _(u"previous")
    else:
        c['previous_page_text'] = _(u"previous")
        c['next_page_text'] = _(u"next")
    return c


_date_formatter = lambda x: x.isoformat() if x is not None else None

@register.inclusion_tag('utils/pagination.html')
def show_gqslpagination_by_date(page, reverse=False):
    c = _base_page_data(page)
    if c['has_previous'] and c['previous_page_number'] is not None:
        c['previous_page_number'] = c['previous_page_number'].isoformat()
    if c['has_next'] and c['next_page_number'] is not None:
        c['next_page_number'] = c['next_page_number'].isoformat()
    if reverse:
        c['previous_page_text'] = _(u"newer")
        c['next_page_text'] = _(u"older")
    else:
        c['previous_page_text'] = _(u"older")
        c['next_page_text'] = _(u"newer")
    return c
