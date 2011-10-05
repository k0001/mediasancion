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

from django.conf.urls.defaults import *


# congreso:proyectos:
urlpatterns_proyectos = patterns('mediasancion.congreso.views',
    url(r'^$',
        'proyecto_list',
        name='list'),
)

# congreso:diputados:proyectos:
# congreso:senadores:proyectos:
urlpatterns_camara_proyectos = patterns('mediasancion.congreso.views',
    url(r'^$',
        'proyecto_list',
        name='list'),

    url(r'^(?P<expediente>[-\w]+)/$',
        'proyecto_detail',
        name='detail'),
)

# congreso:comisiones:
urlpatterns_comisiones = patterns('mediasancion.congreso.views',
    url(r'^$',
        'comision_list',
        name='list'),
)

# congreso:diputados:comisiones:
# congreso:senadores:comisiones:
urlpatterns_camara_comisiones = patterns('mediasancion.congreso.views',
    url(r'^$',
        'comision_list_by_camara',
        name='list'),

    url(r'^(?P<slug>[-\w]+)/$',
        'comision_detail',
        name='detail'),
)


# congreso:legisladores:
# congreso:diputados:legisladores:
# congreso:senadores:legisladores:
urlpatterns_legisladores = patterns('mediasancion.congreso.views',
    url(r'^$',
        'legislador_list',
        name='list'),
)


# congreso:diputados:
# congreso:senadores:
urlpatterns_camara = patterns('',
    url(r'^$',
        'mediasancion.congreso.views.camara_detail',
        name='detail'),

    url(r'^proyectos/',
        include(urlpatterns_camara_proyectos,
                namespace='proyectos', app_name='congreso')),

    url(r'^comisiones/',
        include(urlpatterns_camara_comisiones,
                namespace='comisiones', app_name='congreso')),

    url(r'^legisladores/',
        include(urlpatterns_legisladores,
                namespace='legisladores', app_name='congreso')),
)


# congreso:
urlpatterns = patterns('',
    url(r'^senadores/',
        include(urlpatterns_camara,
                namespace='senadores', app_name='congreso'),
        {'camara': 'S'}),

    url(r'^diputados/',
        include(urlpatterns_camara,
                namespace='diputados', app_name='congreso'),
        {'camara': 'D'}),

    url(r'^comisiones/',
        include(urlpatterns_comisiones,
                namespace='comisiones', app_name='congreso')),

    url(r'^proyectos/',
        include(urlpatterns_proyectos,
                namespace='proyectos', app_name='congreso')),

    url(r'^legisladores/',
        include(urlpatterns_legisladores,
                namespace='legisladores', app_name='congreso')),

)
