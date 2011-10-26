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

from datetime import datetime
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from .models import Bloque, Persona
from ..congreso.models import Legislador


def bloque_list(request):
    qs = Bloque.objects.all()

    # NOTE By default we list only Bloque objects with at least a Legislador
    #      currently active.
    utcnow = datetime.utcnow()
    qs = qs.filter(legislador__inicio__lte=utcnow,
                   legislador__fin__gte=utcnow)

    qs = qs.select_related('legislador') \
           .annotate(Count('legislador')) \
           .order_by('nombre') \

    bloques = qs.all()

    c = { 'title': _(u"Bloques"),
          'bloques': bloques }

    return render_to_response('core/bloque_list.html', c,
                              context_instance=RequestContext(request))


def bloque_detail(request, slug):
    bloque = get_object_or_404(Bloque, slug=slug)

    bloque.denorm_legisladores = \
        Legislador.current.filter(bloque=bloque) \
                          .select_related('persona') \
                          .order_by('persona__apellido',
                                    'persona__nombre')

    breadcrumbs = (
        (reverse('core:bloques:list'), _(u"Bloques")), )

    c = { 'title': bloque.nombre,
          'bloque': bloque }

    return render_to_response('core/bloque_detail.html', c,
                              context_instance=RequestContext(request))



def distrito_list(request):
    pass

def distrito_detail(request, slug):
    pass

def persona_detail(request, slug):
    persona = get_object_or_404(Persona, slug=slug)

    now = datetime.utcnow()
    try:
        legislador_current = persona.legislador_set.get(inicio__lte=now, fin__gte=now)
    except Legislador.DoesNotExist:
        legislador_current = None

    legislador_past_list = persona.legislador_set.order_by('-fin', '-inicio')
    if legislador_current:
        legislador_past_list = legislador_past_list.exclude(pk=legislador_current.pk)

    c = { 'title': persona.full_name,
          'persona': persona,
          'legislador_current': legislador_current,
          'legislador_past_list': legislador_past_list }

    return render_to_response('core/persona_detail.html', c,
                              context_instance=RequestContext(request))
