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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField, UUIDField

from mediasancion.utils.models import StandardAbstractModel


class Distrito(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    nombre = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from='nombre')

    def __unicode__(self):
        return self.nombre

    @models.permalink
    def get_absolute_url(self):
        return 'core:distritos:detail', (self.slug,)

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:core:distritos:detail', (self.uuid,)

    class Meta:
        verbose_name = _(u"distrito")
        verbose_name_plural = _(u"distritos")


class Partido(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    nombre = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre', overwrite=True)

    def __unicode__(self):
        return self.nombre

    @models.permalink
    def get_absolute_url(self):
        return 'core:partidos:detail', (self.slug,)

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:core:partidos:detail', (self.uuid,)

    class Meta:
        verbose_name = _(u"partido político")
        verbose_name_plural = _(u"partidos políticos")


class Bloque(StandardAbstractModel):
    uuid = UUIDField(version=4, unique=True, db_index=True)
    nombre = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre', overwrite=True)

    def __unicode__(self):
        return self.nombre

    @models.permalink
    def get_absolute_url(self):
        return 'core:bloque:detail', (self.slug,)

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:core:bloques:detail', (self.uuid,)

    class Meta:
        verbose_name = _(u"bloque político")
        verbose_name_plural = _(u"bloques políticos")


class Persona(StandardAbstractModel):
    TIPO_DOCUMENTO_CHOICES = (
        ('D', _(u"D.N.I.")), )

    uuid = UUIDField(version=4, unique=True, db_index=True)
    slug = AutoSlugField(populate_from=('apellido', 'nombre'), overwrite=True)
    nombre = models.CharField(max_length=128)
    apellido = models.CharField(max_length=128)
    documento_tipo = models.CharField(max_length=1, choices=TIPO_DOCUMENTO_CHOICES, null=True, blank=True)
    documento_numero = models.CharField(max_length=63, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=32, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    foto = models.ImageField(null=True, blank=True, upload_to='persona-foto/')

    @property
    def identity(self):
        if self.documento_tipo and self.documento_numero:
            return u'%s %s' % (self.get_documento_tipo_display, self.documento_numero)

    @property
    def full_name(self):
        return u'%s, %s' % (self.nombre, self.apellido)

    def __unicode__(self):
        return self.full_name

    @property
    @models.permalink
    def api0_url(self):
        return 'api0:core:personas:detail', (self.uuid,)

    def save(self, *args, **kwargs):
        # Somehow forbid adding a partial identity
        if self.documento_tipo or self.documento_numero:
            assert self.documento_tipo and self.documento_numero
        super(Persona, self).save(*args, **kwargs)
