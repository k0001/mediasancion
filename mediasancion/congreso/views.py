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

from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .models import Proyecto, CAMARA_CHOICES_DISPLAYS, CAMARA_CHOICES_SLUGS
from django_gqslpagination import GroupedQuerySetLaxPaginator, EmptyPage


def camara_detail(request, camara):
    pass



def proyecto_list(request, camara=None):
    if camara in ('D', 'S'):
        qs = Proyecto.objects.filter(camara_origen=camara)
        show_camera = False
    else:
        qs = Proyecto.objects.all()
        show_camera = True

    qs = qs.order_by('-fecha')

    try:
        # Paginamos místicamente por fecha:
        paginator = GroupedQuerySetLaxPaginator(qs, 'publicacion_fecha', lax_want=40,
                                                lax_threshold=0.3, reverse=True)
        pag = request.GET.get('pag')
        page = paginator.page(pag)
    except EmptyPage:
        raise Http404

    breadcrumbs = []
    if camara:
        breadcrumbs.append(
            (reverse('congreso:%s:detail' % CAMARA_CHOICES_SLUGS[camara]),
                 CAMARA_CHOICES_DISPLAYS[camara]))

    c = {
        'title': _(u"Proyectos"),
        'breadcrumbs': breadcrumbs,
        'page': page }

    return render_to_response('congreso/proyecto_list.html', c,
                              context_instance=RequestContext(request))

def proyecto_detail(request, camara, expediente):
    # no hay necesidad de filtrar por `camara` también, `codigo_expediente` es UNIQUE
    proyecto = get_object_or_404(Proyecto, codigo_expediente=expediente)

    breadcrumbs = (
        (reverse('congreso:%s:detail' % proyecto.camara_origen_slug),
            proyecto.get_camara_origen_display()),
        (reverse('congreso:%s:proyectos:list' % proyecto.camara_origen_slug),
            _(u"Proyectos")), )

    c = {
        'title': unicode(proyecto),
        'breadcrumbs': breadcrumbs,
        'proyecto': proyecto }

    return render_to_response('congreso/proyecto_detail.html', c,
                              context_instance=RequestContext(request))




def comision_list(request, camara=None):
    pass

def comision_detail(request, camara, slug):
    pass

def legislador_list(request, camara=None):
    pass

def legislador_detail(request, slug):
    pass
