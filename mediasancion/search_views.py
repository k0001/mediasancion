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

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

import haystack

from .search_forms import MSSearchForm




def split_searchqueryset_by_contenttype(sqs, site=haystack.site):
    cts = ['%s.%s' % (m._meta.app_label, m._meta.module_name)
           for m in site.get_indexed_models()]
    ct_field = haystack.constants.DJANGO_CT
    return dict((ct, sqs.filter(**{ct_field: ct})) for ct in cts)


# I WAS REALLY TIRED WHEN I WROTE THE FOLLOWING LINES. SORRY ABOUT THE MESS.
def search(request):
    c = {}
    c['form'] = form = MSSearchForm(request.GET)

    if not form.is_valid():
        print form.errors
        raise Http404 # Is OK. This shouldn't happen anyway (unless punks?)

    c['query'] = query = form.cleaned_data.get('q')
    if query:
        sqs = form.search()

        try:
            c['page_num'] = page_num = int(request.GET.get('page', 1))
        except ValueError:
            raise Http404

        c['all_results_count'] = 0
        c['current_page_results_count'] = 0
        c['results'] = {}

        sqs_per_ct = split_searchqueryset_by_contenttype(sqs)

        # Proyectos
        proyectos_sqs = sqs_per_ct['congreso.proyecto']
        pts = form.cleaned_data.get('proyecto_tipo')
        if pts:
            proyectos_sqs = proyectos_sqs.filter(tipo__in=pts)
            c['all_results_count'] += len(proyectos_sqs)

        # Non proyectos
        if page_num == 1: # We don't show non-Proyectos results in non-first pages.
            for k,v in sqs_per_ct.items():
                v1 = v.load_all()
                c['results'][k.replace('.', '_')] = v1
                v1_length = len(v1)
                c['current_page_results_count'] += v1_length
                c['all_results_count'] += v1_length


        # paginate proyectos
        proyectos_paginator = Paginator(proyectos_sqs.load_all(), 30,
                                        allow_empty_first_page=True)
        try:
            proyectos_page = proyectos_paginator.page(page_num)
        except InvalidPage:
            raise Http404

        c['results']['congreso_proyecto'] = {'paginator': proyectos_paginator,
                                             'page': proyectos_page}

        if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
            c['suggestion'] = form.get_suggestion()

        c['breadcrumbs'] = (
            (reverse('search'), _(u"Búsqueda")),)

        return render_to_response('search/search.html', c,
                                  context_instance=RequestContext(request))












