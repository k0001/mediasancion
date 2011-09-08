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

import os
from datetime import date

import Image

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField, UUIDField

from mediasancion.utils.models import StandardAbstractModel


CAMARA_CHOICES = (
    (ord('S'), _(u"senadores")),
    (ord('D'), _(u"diputados")), )
CAMARA_CHOICES_DISPLAYS = dict(CAMARA_CHOICES)
CAMARA_CHOICES_SLUGS = {
    ord('S'): u'senadores',
    ord('D'): u'diputados' }


class Comision(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    camara = models.IntegerField(choices=CAMARA_CHOICES)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='nombre', overwrite=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = _(u"comisión")
        verbose_name_plural = _(u"comisiones")
        unique_together = ('camara', 'nombre')

    @property
    def camara_slug(self):
        return CAMARA_CHOICES_SLUGS[self.camara]

    @models.permalink
    def get_absolute_url(self):
        return 'congreso:%s:comisiones:detail' % self.camara_slug, (self.slug,)

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:congreso:comisiones:detail', (self.uuid,)


class Legislador(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    persona = models.ForeignKey('core.Persona', null=True)
    camara = models.IntegerField(choices=CAMARA_CHOICES) # ord('?') could mean we don't know.
    # XXX inicio, fin, partido and distrito shouldn't be null, but we have some missing data.
    inicio = models.DateField(null=True)
    fin = models.DateField(null=True)
    partido = models.ForeignKey('core.Partido', null=True)
    bloque = models.ForeignKey('core.Bloque', null=True)
    distrito = models.ForeignKey('core.Distrito', null=True)

    class Meta:
        ordering = '-fin', '-inicio'

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:congreso:legisladores:detail', (self.uuid,)

    def __unicode__(self):
        out = u'%s: %s' % (self.persona.full_name, self.get_camara_display())
        if self.inicio and self.fin:
            out += u' %s-%s' % (self.inicio.strftime('%Y'), self.fin.strftime('%Y'))
        return out

    def save(self, *args, **kwargs):
        if self.inicio and self.fin and not self.inicio <= self.fin:
            raise ValueError('%s > %s' % (self.inicio, self.fin))
        return super(Legislador, self).save(*args, **kwargs)


class MembresiaComision(StandardAbstractModel):
    CARGO_CHOICES = (
        (ord('P'), _(u'presidente')),
        (ord('Q'), _(u'vicepresidente 1ro')),
        (ord('R'), _(u'vicepresidente 2do')),
        (ord('S'), _(u'secretario')),
        (ord('V'), _(u'vocal')), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    legislador = models.ForeignKey(Legislador, null=True)
    comision = models.ForeignKey(Comision)
    cargo = models.IntegerField(choices=CARGO_CHOICES)


class Reunion(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    camara = models.IntegerField(choices=CAMARA_CHOICES)
    nro_periodo = models.IntegerField()
    nro_reunion = models.IntegerField()
    titulo = models.CharField(max_length=128)
    fecha = models.DateField()


class AsistenciaReunion(StandardAbstractModel):
    ASISTENCIA_CHOICES = (
        (ord('P'), _(u'presente')),
        (ord('A'), _(u'ausente con aviso')),
        (ord('L'), _(u'licencia')),
        (ord('M'), _(u'mision Oficial')), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    reunion = models.ForeignKey(Reunion)
    legislador = models.ForeignKey(Legislador, null=True)
    asistencia = models.IntegerField(choices=ASISTENCIA_CHOICES)


class Proyecto(StandardAbstractModel):
    TIPO_CHOICES = (
        (ord('L'), _(u'ley')),
        (ord('D'), _(u'declaración')),
        (ord('R'), _(u'resolución')),
        (ord('C'), _(u'comunicación')),
        (ord('E'), _(u'decreto')),
        (ord('M'), _(u'mensaje')), )

    ORIGEN_CHOICE = (
        (ord('S'), _(u"cámara de senadores")),
        (ord('D'), _(u"cámara de diputados")),
        (ord('E'), _(u"poder ejecutivo")),
        (ord('J'), _(u"jefe de gabinete")),
        (ord('O'), _(u"organismos oficiales")),
        (ord('P'), _(u"particular")), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    origen = models.IntegerField(choices=ORIGEN_CHOICE)
    camara_origen = models.IntegerField(choices=CAMARA_CHOICES)
    camara_origen_expediente = models.CharField(max_length=15)
    camara_revisora = models.IntegerField(choices=CAMARA_CHOICES, null=True, blank=True)
    camara_revisora_expediente = models.CharField(max_length=15)
    tipo = models.IntegerField(choices=TIPO_CHOICES)
    tipo_verbose = models.CharField(max_length=255)
    mensaje = models.CharField(max_length=15)
    sumario = models.TextField(blank=True)
    fundamentos = models.TextField(blank=True)
    firmantes = models.ManyToManyField(Legislador, through='FirmaProyecto')
    comisiones = models.ManyToManyField(Comision)
    texto_completo_url = models.URLField()
    texto_mediasancion_senadores_url = models.URLField()
    texto_mediasancion_diputados_url = models.URLField()
    publicacion_en = models.CharField(max_length=255)
    publicacion_fecha = models.DateField()
    reproduccion_expediente = models.CharField(max_length=16, blank=True)
    ley_numero = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('camara_origen', 'camara_origen_expediente'),

    def __unicode__(self):
        return _(u"Proyecto de %(tipo)s %(camara_origen_expediente)s") % {
                        'tipo': self.get_tipo_display().capitalize(),
                        'camara_origen_expediente': self.camara_origen_expediente }

    @models.permalink
    def get_absolute_url(self):
        return 'congreso:%s:proyectos:detail' % self.camara_origen_slug, (self.camara_origen_expediente,)

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:congreso:proyectos:detail', (self.uuid,)


    @property
    def camara_origen_slug(self):
        return CAMARA_CHOICES_SLUGS[self.camara_origen]


class FirmaProyecto(StandardAbstractModel):
    TIPO_FIRMA_CHOICES = (
        (ord('F'), _(u'Firmante')),
        (ord('C'), _(u'Cofirmante')), )

    PODER_CHOICES = (
        (ord('L'), _(u"legislativo")),
        (ord('E'), _(u"ejecutivo")), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    poder = models.IntegerField(choices=PODER_CHOICES)
    legislador = models.ForeignKey(Legislador, null=True) # null if poder ejecutivo, probably
    proyecto = models.ForeignKey(Proyecto)
    tipo_firma = models.IntegerField(choices=TIPO_FIRMA_CHOICES)

    # XXX REMOVE THIS FIELD: Well, not sure if it can be done, but maybe once we have a Personaa model
    poder_who =  models.CharField(max_length=255, blank=True)


    class Meta:
        unique_together = ('legislador', 'proyecto')
