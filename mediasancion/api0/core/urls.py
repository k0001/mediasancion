# coding: utf-8

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

from __future__ import absolute_import

from django.conf.urls.defaults import *

from restsources import Handler
from restsources.restponders.json import JSONRestponder, JSONPRestponder
from restsources.restponders.xml import XMLRestponder

from .restsources import DistritoRestsource, PartidoRestsource, BloqueRestsource, PersonaRestsource


handler = Handler([JSONRestponder(), JSONPRestponder(), XMLRestponder()])



# URL namespace: api0:core:distritos
urlpatterns_distritos = patterns('',
    url(r'^$',
        handler,
        {'handler_options': {'restsource':
        DistritoRestsource(primary_fields_only=True)}},
        name='list'),

    url(r'^(?P<uuid>.+)/$',
        handler,
        {'handler_options': {'restsource': DistritoRestsource(), 'single': True}},
        name='detail'),
)


# URL namespace: api0:core:partidos
urlpatterns_partidos = patterns('',
    url(r'^$',
        handler,
        {'handler_options': {'restsource': PartidoRestsource(primary_fields_only=True)}},
        name='list'),

    url(r'^(?P<uuid>.+)/$',
        handler,
        {'handler_options': {'restsource': PartidoRestsource(), 'single': True}},
        name='detail'),
)


# URL namespace: api0:core:bloques
urlpatterns_bloques = patterns('',
    url(r'^$',
        handler,
        {'handler_options': {'restsource': BloqueRestsource(primary_fields_only=True)}},
        name='list'),

    url(r'^(?P<uuid>.+)/$',
        handler,
        {'handler_options': {'restsource': BloqueRestsource(), 'single': True}},
        name='detail'),
)

# URL namespace: api0:core:personas
urlpatterns_personas = patterns('',
    url(r'^$',
        handler,
        {'handler_options': {'restsource': PersonaRestsource(primary_fields_only=True)}},
        name='list'),

    url(r'^(?P<uuid>.+)/$',
        handler,
        {'handler_options': {'restsource': PersonaRestsource(), 'single': True}},
        name='detail'),
)

# URL namespace: api0:core
urlpatterns = patterns('',
    url(r'^distritos/', include(urlpatterns_distritos,
                                namespace='distritos', app_name='api0')),

    url(r'^partidos/', include(urlpatterns_partidos,
                                namespace='partidos', app_name='api0')),

    url(r'^bloques/', include(urlpatterns_bloques,
                                namespace='bloques', app_name='api0')),

    url(r'^personas/', include(urlpatterns_personas,
                                namespace='personas', app_name='api0')),
)
