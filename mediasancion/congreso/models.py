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
from datetime import date, datetime

import Image

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField, UUIDField

from mediasancion.utils.models import StandardAbstractModel


CAMARA_CHOICES = (
    ('S', _(u"Senadores")),
    ('D', _(u"Diputados")), )
CAMARA_CHOICES_DISPLAYS = dict(CAMARA_CHOICES)
CAMARA_CHOICES_LONG_DISPLAYS = {
    'S': _(u"Cámara de Senadores"),
    'D': _(u"Cámara de Diputados") }
CAMARA_CHOICES_SLUGS = {
    'S': u'senadores',
    'D': u'diputados' }


class Comision(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    camara = models.CharField(max_length=1, choices=CAMARA_CHOICES)
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


class CurrentLegisladorManager(models.Manager):
    def get_query_set(self):
        now = datetime.now()
        return super(CurrentLegisladorManager, self) \
            .get_query_set().filter(inicio__lte=now, fin__gte=now)


class Legislador(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    persona = models.ForeignKey('core.Persona', null=True)
    camara = models.CharField(max_length=1, choices=CAMARA_CHOICES) # '?' could mean we don't know.
    # XXX inicio, fin, partido and distrito shouldn't be null, but we have some missing data.
    inicio = models.DateField(null=True)
    fin = models.DateField(null=True)
    partido = models.ForeignKey('core.Partido', null=True)
    bloque = models.ForeignKey('core.Bloque', null=True)
    distrito = models.ForeignKey('core.Distrito', null=True)

    objects = models.Manager()
    current = CurrentLegisladorManager()

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

    @property
    def tipo_display(self):
        if self.camara == 'S':
            return _(u"Senador")
        elif self.camara == 'D':
            return _(u"Diputado")
        else:
            return _(u"Legislador")


    def save(self, *args, **kwargs):
        if self.inicio and self.fin and not self.inicio <= self.fin:
            raise ValueError('%s > %s' % (self.inicio, self.fin))
        return super(Legislador, self).save(*args, **kwargs)


class MembresiaComision(StandardAbstractModel):
    CARGO_CHOICES = (
        ('P', _(u'presidente')),
        ('Q', _(u'vicepresidente 1ro')),
        ('R', _(u'vicepresidente 2do')),
        ('S', _(u'secretario')),
        ('V', _(u'vocal')), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    legislador = models.ForeignKey(Legislador, null=True)
    comision = models.ForeignKey(Comision)
    cargo = models.CharField(max_length=1, choices=CARGO_CHOICES)


class Reunion(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    camara = models.CharField(max_length=1, choices=CAMARA_CHOICES)
    nro_periodo = models.IntegerField()
    nro_reunion = models.IntegerField()
    titulo = models.CharField(max_length=128)
    fecha = models.DateField()


class AsistenciaReunion(StandardAbstractModel):
    ASISTENCIA_CHOICES = (
        ('P', _(u'presente')),
        ('A', _(u'ausente con aviso')),
        ('L', _(u'licencia')),
        ('M', _(u'mision oficial')), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    reunion = models.ForeignKey(Reunion)
    legislador = models.ForeignKey(Legislador, null=True)
    asistencia = models.CharField(max_length=1, choices=ASISTENCIA_CHOICES)


class Proyecto(StandardAbstractModel):
    TIPO_CHOICES = (
        ('L', _(u'ley')),
        ('D', _(u'declaración')),
        ('R', _(u'resolución')),
        ('C', _(u'comunicación')),
        ('E', _(u'decreto')),
        ('M', _(u'mensaje')), )

    ORIGEN_CHOICE = (
        ('S', _(u"cámara de senadores")),
        ('D', _(u"cámara de diputados")),
        ('E', _(u"poder ejecutivo")),
        ('J', _(u"jefe de gabinete")),
        ('O', _(u"organismos oficiales")),
        ('P', _(u"particular")), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    origen = models.CharField(max_length=1, choices=ORIGEN_CHOICE)
    camara_origen = models.CharField(max_length=1, choices=CAMARA_CHOICES)
    camara_origen_expediente = models.CharField(max_length=15)
    camara_revisora = models.CharField(max_length=1, choices=CAMARA_CHOICES, null=True, blank=True)
    camara_revisora_expediente = models.CharField(max_length=15)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    tipo_verbose = models.CharField(max_length=255)
    mensaje = models.CharField(max_length=15)
    sumario = models.TextField(blank=True)
    fundamentos = models.TextField(blank=True)
    firmantes_set = models.ManyToManyField(Legislador, through='FirmaProyecto')
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
        if self.camara_revisora:
            camara_revisora_text = u" → %s" % self.camara_revisora_expediente
        else:
            camara_revisora_text = u""
        return (u"Proyecto de %(tipo)s %(camara_origen_expediente)s"
                u"%(camara_revisora_text)s") % {
                        'tipo': self.get_tipo_display().capitalize(),
                        'camara_origen_expediente': self.camara_origen_expediente,
                        'camara_revisora_text': camara_revisora_text }

    def get_absolute_url(self):
        return self.get_origen_pov_absolute_url()

    @models.permalink
    def get_origen_pov_absolute_url(self):
        return 'congreso:%s:proyectos:detail' % self.camara_origen_slug, (self.camara_origen_expediente,)

    @models.permalink
    def get_revisora_pov_absolute_url(self):
        if self.camara_revisora:
            return 'congreso:%s:proyectos:detail' % self.camara_revisora_slug, (self.camara_revisora_expediente,)

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:congreso:proyectos:detail', (self.uuid,)


    @property
    def camara_origen_slug(self):
        return CAMARA_CHOICES_SLUGS[self.camara_origen]

    @property
    def camara_revisora_slug(self):
        if self.camara_revisora:
            return CAMARA_CHOICES_SLUGS[self.camara_revisora]

    @property
    def firmante(self):
        return self.firmantes_set.get(firmaproyecto__tipo_firma='F')

    @property
    def cofirmantes(self):
        return self.firmantes_set.filter(firmaproyecto__tipo_firma='C')


class FirmaProyecto(StandardAbstractModel):
    TIPO_FIRMA_CHOICES = (
        ('F', _(u'firmante')),
        ('C', _(u'cofirmante')), )

    PODER_CHOICES = (
        ('L', _(u"legislativo")),
        ('E', _(u"ejecutivo")), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    poder = models.CharField(max_length=1, choices=PODER_CHOICES)
    legislador = models.ForeignKey(Legislador, null=True) # null if poder ejecutivo, probably
    proyecto = models.ForeignKey(Proyecto)
    tipo_firma = models.CharField(max_length=1, choices=TIPO_FIRMA_CHOICES)

    # XXX REMOVE THIS FIELD: Well, not sure if it can be done, but maybe once we have a Personaa model
    poder_who =  models.CharField(max_length=255, blank=True)


    class Meta:
        unique_together = ('legislador', 'proyecto')

        # quick hack so that firmantes come before cofirmantes by default, and
        # so that poder ejecutivo comes fefore poder legislativo
        ordering = ('-tipo_firma', 'poder')


class DictamenProyecto(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    proyecto = models.ForeignKey(Proyecto)
    camara = models.CharField(max_length=1, choices=CAMARA_CHOICES)
    orden_del_dia = models.CharField(max_length=9, blank=True)
    resultado = models.TextField()
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(null=True, blank=True)
    # since not every dictamen has an associated fecha, we need to keep an
    # index so we can later sort them.
    index = models.PositiveIntegerField()

    class Meta:
        unique_together = ('proyecto', 'index'),
        ordering = 'index',
