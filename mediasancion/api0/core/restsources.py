# coding: utf-8

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

from restsources import Handler, Restsource

from mediasancion.core.models import Distrito, Partido, Bloque, Persona


__all__ = 'DistritoRestsource', 'PartidoRestsource', 'BloqueRestsource', 'PersonaRestsource',


class DistritoRestsource(Restsource):
    model = Distrito
    name = 'distrito'
    name_plural = 'distritos'

    primary_fields = (
        'url',
        'uuid')

    fields = (
        'nombre',
        'legisladores',
        'remote_source',
        'remote_url',
        'remote_id')

    @property
    def relations(self):
        from ..congreso.restsources import LegisladorRestsource
        return {
            'legisladores': LegisladorRestsource(primary_fields_only=True) }

    def get_url(self, obj):
        return obj.api0_url

    def get_legisladores(self, obj):
        return obj.legislador_est

    def filter(self, queryset, request, **params):
        if request.REQUEST.get('nombre'):
            queryset = queryset.filter(nombre__icontains=request.REQUEST['nombre'])
        return queryset.filter(**params)


class PartidoRestsource(Restsource):
    model = Partido
    name = u'partido'
    name_plural = u'partidos'

    primary_fields = (
        'url',
        'uuid')

    fields = (
        'nombre',
        'legisladores',
        'remote_source',
        'remote_url',
        'remote_id')

    @property
    def relations(self):
        from ..congreso.restsources import LegisladorRestsource
        return {
            'legisladores': LegisladorRestsource(primary_fields_only=True), }

    def get_url(self, obj):
        return obj.api0_url

    def get_legisladores(self, obj):
        return obj.legislador_est

    def filter(self, queryset, request, **params):
        if request.REQUEST.get('nombre'):
            queryset = queryset.filter(nombre__icontains=request.REQUEST['nombre'])
        return queryset.filter(**params)


class BloqueRestsource(Restsource):
    model = Bloque
    name = u'bloque'
    name_plural = u'bloques'

    primary_fields = (
        'url',
        'uuid')

    fields = (
        'nombre',
        'legisladores',
        'remote_source',
        'remote_url',
        'remote_id')

    @property
    def relations(self):
        from ..congreso.restsources import LegisladorRestsource
        return {
            'legisladores': LegisladorRestsource(primary_fields_only=True) }

    def get_url(self, obj):
        return obj.api0_url

    def get_legisladores(self, obj):
        return obj.legislador_set

    def filter(self, queryset, request, **params):
        if request.REQUEST.get('nombre'):
            queryset = queryset.filter(nombre__icontains=request.REQUEST['nombre'])
        return queryset.filter(**params)


class PersonaRestsource(Restsource):
    model = Persona
    name = u'persona'
    name_plural = u'personas'

    primary_fields = (
        'url',
        'uuid')

    fields = (
        'nombre',
        'apellido',
        'documento_tipo',
        'documento_numero',
        'email',
        'telefono',
        'website',
        'foto',
        'legisladores',
        'remote_source',
        'remote_url',
        'remote_id')

    @property
    def relations(self):
        from ..congreso.restsources import LegisladorRestsource
        return {
            'legisladores': LegisladorRestsource(primary_fields_only=True) }

    def get_url(self, obj):
        return obj.api0_url

    def get_legisladores(self, obj):
        return obj.legislador_set

    def filter(self, queryset, request, **params):
        if request.REQUEST.get('nombre'):
            queryset = queryset.filter(nombre__icontains=request.REQUEST['nombre'])
        if request.REQUEST.get('apellido'):
            queryset = queryset.filter(apellido__icontains=request.REQUEST['apellido'])
        if request.REQUEST.get('documento_tipo'):
            queryset = queryset.filter(documento_tipo=request.REQUEST['documento_tipo'])
        if request.REQUEST.get('documento_numero'):
            queryset = queryset.filter(documento_numero=request.REQUEST['documento_numero'])
        if request.REQUEST.get('email'):
            queryset = queryset.filter(email=request.REQUEST['email'])
        if request.REQUEST.get('telefono'):
            queryset = queryset.filter(telefono=request.REQUEST['telefono'])
        if request.REQUEST.get('website'):
            queryset = queryset.filter(website=request.REQUEST['website'])
        return queryset.filter(**params)

