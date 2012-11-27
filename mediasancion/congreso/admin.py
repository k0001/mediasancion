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

from django.contrib import admin

from mediasancion.congreso.models import Legislador, Comision, MembresiaComision, Proyecto, FirmaProyecto


class FirmaProyectoInline(admin.TabularInline):
    model = FirmaProyecto
    extra = 1


class MembresiaComisionInline(admin.TabularInline):
    model = MembresiaComision
    extra = 1


class ComisionAdmin(admin.ModelAdmin):
    inlines = MembresiaComisionInline,


class ProyectoAdmin(admin.ModelAdmin):
    inlines = FirmaProyectoInline,
    filter_horizontal = 'comisiones',


class LegisladorAdmin(admin.ModelAdmin):
    list_display = 'persona', 'partido', 'distrito', 'inicio', 'fin'


admin.site.register(Legislador, LegisladorAdmin)
admin.site.register(Comision, ComisionAdmin)
admin.site.register(Proyecto, ProyectoAdmin)

