# coding: utf8

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

from __future__ import absolute_import

import isodate

from restsources import Handler, Restsource, Restponse, RESTPONSE_STATUS
from restsources.shortcuts import payload_from_form_errors

from django.conf import settings

from mediasancion.congreso.models import Proyecto, Comision, Legislador, \
            MembresiaComision, FirmaProyecto, CAMARA_SLUGS
from mediasancion.api0.core.restsources import DistritoRestsource, PartidoRestsource, \
            BloqueRestsource,PersonaRestsource


class LegisladorRestsource(Restsource):
    model = Legislador
    name = 'legislador'
    name_plural = 'legisladores'

    primary_fields = (
        'uuid',
        'url')

    fields = (
        'inicio',
        'fin',
        'camara',
        'persona',
        'partido',
        'bloque',
        'distrito',
        'membresias_comisiones',
        'firmas_proyectos',
        'remote_source',
        'remote_url',
        'remote_id')

    @property
    def relations(self):
        return {
            'persona': PersonaRestsource(excluded=['legisladores'], primary_fields_only=True),
            'partido': PartidoRestsource(excluded=['legisladores'], primary_fields_only=True),
            'bloque': BloqueRestsource(excluded=['legisladores'], primary_fields_only=True),
            'distrito': DistritoRestsource(excluded=['legisladores'], primary_fields_only=True),
            'membresias_comisiones': MembresiaComisionRestsource(excluded=['legislador']),
            'firmas_proyectos': FirmaProyectoRestsource(excluded=['legislador']) }

    def get_firmas_proyectos(self, obj):
        return obj.firmaproyecto_set

    def get_membresias_comisiones(self, obj):
        return obj.membresiacomision_set

    def get_url(self, obj):
        return obj.api0_url

    def filter(self, queryset, request, **params):
        if request.REQUEST.get('camara'):
            queryset = queryset.filter(camara=request.REQUEST['camara'])
        if request.REQUEST.get('partido'):
            queryset = queryset.filter(partido__uuid=request.REQUEST['partido'])
        if request.REQUEST.get('persona'):
            queryset = queryset.filter(persona__uuid=request.REQUEST['persona'])
        if request.REQUEST.get('distrito'):
            queryset = queryset.filter(distrito__uuid=request.REQUEST['distrito'])
        return queryset.filter(**params)


class ComisionRestsource(Restsource):
    model = Comision
    name = 'comision'
    name_plural = 'comisiones'

    primary_fields = (
        'uuid',
        'url')

    fields = (
        'camara',
        'nombre',
        'descripcion',
        'membresias',
        'proyectos',
        'remote_source',
        'remote_url',
        'remote_id')

    @property
    def relations(self):
        return {
            'membresias': MembresiaComisionRestsource(excluded=['comision']),
            'proyectos': ProyectoRestsource(primary_fields_only=True, excluded=['comisiones']) }

    def get_url(self, obj):
        return obj.api0_url

    def filter(self, queryset, request, **params):
        if request.REQUEST.get('nombre'):
            queryset = queryset.filter(nombre__icontains=request.REQUEST['nombre'])
        return queryset.filter(**params)



class MembresiaComisionRestsource(Restsource):
    model = MembresiaComision
    name = u'membresia_comision'
    name_plural = u'membresias_comisiones'

    primary_fields = (
        'uuid',)

    fields = (
        'legislador',
        'comision',
        'cargo')

    relations = {
        'legislador': LegisladorRestsource(fields=['legislador']),
        'comision': ComisionRestsource(primary_fields_only=True), }



class FirmaProyectoRestsource(Restsource):
    model = FirmaProyecto
    name = 'firma_proyecto'
    name_plural = 'firmas_proyectos'

    primary_fields = (
        'uuid',)

    fields = (
        'tipo',
        'legislador',
        'proyecto')

    @property
    def relations(self):
        return {
            'legislador': LegisladorRestsource(fields=['legislador']),
            'proyecto': ProyectoRestsource(primary_fields_only=True) }

    def get_tipo(self, obj):
        return obj.tipo_firma


class ProyectoRestsource(Restsource):
    model = Proyecto
    name = 'proyecto'
    name_plural = 'proyectos'

    primary_fields = (
        'uuid',
        'url' )

    fields = (
        'origen',
        'camara_origen',
        'camara_origen_expediente',
        'camara_revisora',
        'camara_revisora_expediente',
        'tipo',
        'mensaje',
        'sumario',
        'fundamentos',
        'firmantes',
        'comisiones',
        'texto_completo_url',
        'texto_mediasancion_senadores_url',
        'texto_mediasancion_diputados_url',
        'publicacion_en',
        'publicacion_fecha',
        'reproduccion_expediente',
        'ley_numero',
        'remote_source',
        'remote_url',
        'remote_id')

    relations = {
        'comisiones': ComisionRestsource(primary_fields_only=True),
        'firmantes': FirmaProyectoRestsource(excluded=['proyecto']) }

    def get_url(self, obj):
        return obj.api0_url

