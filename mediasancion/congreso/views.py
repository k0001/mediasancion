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

from datetime import datetime
from django.db.models import Q, Count
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .models import (Comision, Proyecto, Legislador,
                     CAMARA_DISPLAYS_SHORT, CAMARA_SLUGS)
from .templatetags.congreso import camara_slug, camara_display_short, camara_display_long, \
          camara_legislador_tipo_display_plural
from django_gqslpagination import GroupedQuerySetLaxPaginator, EmptyPage


def camara_detail(request, camara):
    if not camara in ('S', 'D'):
        raise Http404

    legisladores = Legislador.current.filter(camara=camara)
    comisiones = Comision.objects.filter(camara=camara)
    proyectos_originados = Proyecto.objects.filter(camara_origen=camara)
    proyectos_revisados = Proyecto.objects.filter(camara_revisora=camara)

    camara_slug = CAMARA_SLUGS[camara]

    c = { 'camara': camara,
          'camara_slug': camara_slug,

          'legisladores': legisladores,
          'legisladores_href': reverse('congreso:%s:legisladores:list' % camara_slug),

          'comisiones': comisiones,
          'comisiones_href': reverse('congreso:%s:comisiones:list' % camara_slug),

          'proyectos_originados': proyectos_originados,
          'proyectos_revisados': proyectos_revisados,
          'proyectos_href': reverse('congreso:%s:proyectos:list' % camara_slug) }

    return render_to_response('congreso/camara_detail.html', c,
                              context_instance=RequestContext(request))



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
            (reverse('congreso:%s:detail' % CAMARA_SLUGS[camara]),
                 CAMARA_DISPLAYS_SHORT[camara]))

    c = { 'title': _(u"Proyectos"),
          'breadcrumbs': breadcrumbs,
          'page': page }

    return render_to_response('congreso/proyecto_list.html', c,
                              context_instance=RequestContext(request))

def proyecto_detail(request, camara, expediente):
    proyecto = get_object_or_404(Proyecto,
             Q(camara_origen=camara,
               camara_origen_expediente=expediente) |
             Q(camara_revisora=camara,
               camara_revisora_expediente=expediente))

    # Since a Proyecto might be seen from either the originating camara or the
    # reviewing camara point of views, we keep the current point of view
    # explicit to later alter the content presentation for that context.
    origen_pov = proyecto.camara_origen == camara

    breadcrumbs = (
        (reverse('congreso:%s:detail' % CAMARA_SLUGS[camara]),
            CAMARA_DISPLAYS_SHORT[camara]),
        (reverse('congreso:%s:proyectos:list' % CAMARA_SLUGS[camara]),
            _(u"Proyectos")), )

    title = _(u"Proyecto de %(tipo)s %(expediente)s") % {
                    'tipo': proyecto.get_tipo_display().capitalize(),
                    'expediente': expediente }

    c = { 'title': title,
          'breadcrumbs': breadcrumbs,
          'proyecto': proyecto,
          'origen_pov': origen_pov }

    return render_to_response('congreso/proyecto_detail.html', c,
                              context_instance=RequestContext(request))


def comision_list(request):
    pass



def comision_list_by_camara(request, camara):
    qs = Comision.objects.filter(camara=camara)

    # XXX we disabled this for now since we don't have MembresiaComision data!
    ## NOTE By default we list only Comision objects with at least a Legislador
    ##      currently active.
    #now = datetime.now()
    #qs = qs.filter(membresiacomision__legislador__inicio__lte=now,
    #               membresiacomision__legislador__fin__gte=now)

    qs = qs.select_related('membresiacomision') \
           .annotate(Count('membresiacomision')) \
           .order_by('nombre')

    breadcrumbs = (
        (reverse('congreso:%s:detail' % CAMARA_SLUGS[camara]),
            CAMARA_DISPLAYS_SHORT[camara]), )

    title = _(u"Comisiones en Cámara de %(camara)s") % {
                    'camara': CAMARA_DISPLAYS_SHORT[camara].capitalize() }

    c = { 'title': title,
          'breadcrumbs': breadcrumbs,
          'comision_list': qs }

    return render_to_response('congreso/comision_list_by_camara.html', c,
                              context_instance=RequestContext(request))



def comision_detail(request, camara, slug):
    comision = get_object_or_404(Comision, camara=camara, slug=slug)

    breadcrumbs = (
        (reverse('congreso:%s:detail' % CAMARA_SLUGS[camara]),
            CAMARA_DISPLAYS_SHORT[camara]),
        (reverse('congreso:%s:comisiones:list' % CAMARA_SLUGS[camara]),
            _(u"Comisiones")), )

    c = { 'title': comision.nombre,
          'breadcrumbs': breadcrumbs,
          'comision': comision }

    return render_to_response('congreso/comision_detail.html', c,
                              context_instance=RequestContext(request))



def legislador_list(request, camara=None):
    if not camara in ('S', 'D', None):
        raise Http404

    legisladores = Legislador.current.all()
    breadcrumbs = []

    if camara:
        legisladores = legisladores.filter(camara=camara)
        breadcrumbs.append(
            (reverse('congreso:%s:detail' % CAMARA_SLUGS[camara]),
                CAMARA_DISPLAYS_SHORT[camara]))

    c = { 'title': camara_legislador_tipo_display_plural(camara),
          'breadcrumbs': breadcrumbs,
          'legislador_list': legisladores }

    return render_to_response('congreso/legislador_list.html', c,
                              context_instance=RequestContext(request))
