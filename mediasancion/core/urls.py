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

from django.conf.urls.defaults import *


# core:bloques:
urlpatterns_bloques = patterns('mediasancion.core.views',
    url(r'^$',
        'bloque_list',
        name='list'),

    url(r'^(?P<slug>[-\w]+)/$',
        'bloque_detail',
        name='detail'),
)

# core:distritos:
urlpatterns_distritos = patterns('mediasancion.core.views',
    url(r'^$',
        'distrito_list',
        name='list'),

    url(r'^(?P<slug>[-\w]+)/$',
        'distrito_detail',
        name='detail'),
)

# core:personas:
urlpatterns_distritos = patterns('mediasancion.core.views',
    url(r'^(?P<slug>[-\w]+)/$',
        'persona_detail',
        name='detail'),
)

# core:
urlpatterns = patterns('',
    url(r'^bloques/',
        include(urlpatterns_bloques,
                namespace='bloques', app_name='core')),

    url(r'^distritos/',
        include(urlpatterns_distritos,
                namespace='distritos', app_name='core')),

    url(r'^personas/',
        include(urlpatterns_distritos,
                namespace='personas', app_name='core')),
)
