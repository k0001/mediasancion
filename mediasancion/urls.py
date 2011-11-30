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

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from haystack.views import search_view_factory
from .utils.search_forms import StandardSearchForm

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'mediasancion.views.home', name='home'),

    url(r'^search/$', 'mediasancion.search_views.search',
        name='search'),

    url(r'^api/0/', include('mediasancion.api0.urls',
                            namespace='api0', app_name='api0')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('mediasancion.core.urls',
                     namespace='core', app_name='core')),

    url(r'', include('mediasancion.congreso.urls',
                     namespace='congreso', app_name='congreso')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
            'django.views.static.serve',
            { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True } )
    )

