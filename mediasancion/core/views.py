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
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from .models import Bloque


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

    # Denormalize Legislador objects related to each Bloque, sorting them by name
    for b in bloques:
        b.denorm_legisladores = b.legislador_set.select_related('persona') \
                                                .order_by('persona__apellido',
                                                          'persona__nombre')

    c = { 'title': _(u"Bloques"),
          'bloques': bloques }

    return render_to_response('core/bloque_list.html', c,
                              context_instance=RequestContext(request))


def bloque_detail(request, slug):
    pass

def distrito_list(request):
    pass

def distrito_detail(request, slug):
    pass

def persona_detail(request, slug):
    pass
