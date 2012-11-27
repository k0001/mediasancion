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
from django.views.decorators.csrf import csrf_exempt

from restsources import Handler
from restsources.restponders.json import JSONRestponder, JSONPRestponder
from restsources.restponders.xml import XMLRestponder

from .restsources import ProyectoRestsource, ComisionRestsource, LegisladorRestsource


handler = Handler([JSONRestponder(), JSONPRestponder()]) # , XMLRestponder()])


# URL namespace: api0:congreso:proyectos
urlpatterns_proyectos = patterns('',
    url(r'^$',
        handler,
        {'handler_options': {'restsource': ProyectoRestsource(primary_fields_only=True), 'paginate_by': 50}},
        name='list'),

    url(r'^(?P<uuid>.+)/$',
        handler,
        {'handler_options': {'restsource': ProyectoRestsource(), 'single': True}},
        name='detail'),
)


# URL namespace: api0:congreso:comisiones
urlpatterns_comisiones = patterns('',
    url(r'^$',
        handler,
        {'handler_options': {'restsource': ComisionRestsource(fields=['nombre', 'camara'])}},
        name='list'),

    url(r'^(?P<uuid>.+)/$',
        handler,
        {'handler_options': {'restsource': ComisionRestsource(), 'single': True}},
        name='detail'),

)


# URL namespace: api0:congreso:legisladores
urlpatterns_legisladores = patterns('',
    url(r'^$',
        handler,
        {'handler_options': {'restsource': LegisladorRestsource(primary_fields_only=True)}},
        name='list'),

    url(r'^(?P<uuid>.+)/$',
        handler,
        {'handler_options': {'restsource': LegisladorRestsource(), 'single': True}},
        name='detail'),
)



# URL namespace: api0:congreso
urlpatterns = patterns('',

    url(r'^comisiones/', include(urlpatterns_comisiones,
                                namespace='comisiones', app_name='api0')),

    url(r'^proyectos/', include(urlpatterns_proyectos,
                                namespace='proyectos', app_name='api0')),

    url(r'^legisladores/', include(urlpatterns_legisladores,
                                   namespace='legisladores', app_name='api0')),

)
