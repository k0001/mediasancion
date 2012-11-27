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

from datetime import datetime

from django.db import models
from django.conf import settings

from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField,
                                         UUIDField)

__all__ = ('TimeAuditedAbstractModel', 'RemoteResourceAbstractModel',
           'OriginAuditedAbstractModel', 'StandardAbstractModel')



# This is not needed, but I'm so cool that I'm not letting you FAIL by setting
# this to anything but 'UTC'. Also, TimeAuditedAbstractModel usage will be
# clearer if we use UTC.
assert settings.TIME_ZONE == 'UTC', """set settings.TIME_ZONE to 'UTC'
WARNING Django's time zone handling is flawed.
By setting TIME_ZONE='UTC', we guarantee that the datetimes Django store and
retrieve (not tz-aware) are in UTC. We could then do any tz magic by hand.
It's not the best solution, but at least is consistent.
See http://code.djangoproject.com/ticket/10587
    http://code.djangoproject.com/ticket/2626"""


class TimeAuditedAbstractModel(models.Model):
    """
    Adds ``created_at`` and ``updated_at`` fields to the model.

    ``created_at`` is populated only the very first time an object is saved
    with the current local datetime (not tz-aware).

    ``updated_at`` is updated on every save with the current datetime (not
    tz-aware)
    """
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    class Meta:
        abstract = True


class RemoteResourceAbstractModel(models.Model):
    """
    Adds ``remote_source``, ``remote_url`` and ``remote_id`` optional fields to
    the model.

    ``remote_source`` should specify the source from where the model info comes
    from.  Examples: 'Flickr', 'Twitter', 'Facebook'.

    ``remote_url`` should specify a URL for the resource on the remote source,
    if any.  Examples: 'http://somesource.com/resources/2',
    'http://twitter.com/xxx/statuses/123'.

    ``remote_id`` should specify the ID for the resource on the remote source.
    Examples: '1234', 'some-resource', '0ad3fc294', 'urn:something...'
    """

    remote_source = models.CharField(max_length=255, blank=True)
    remote_url = models.URLField(max_length=1023, verify_exists=False,
                                 blank=True)
    remote_id = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class OriginAuditedAbstractModel(models.Model):
    """
    Adds ``origin`` and ``creator`` optional fields to the model.

    ``origin`` should specify where did the model originated.
    Examples: ``manual``, ``api0`.

    ``creator`` should specify the User that created the resource.
    """

    origin = models.CharField(max_length=255, blank=True)
    creator = models.ForeignKey('auth.User', null=True)

    class Meta:
        abstract = True


class StandardAbstractModel(TimeAuditedAbstractModel,
                            RemoteResourceAbstractModel,
                            OriginAuditedAbstractModel):
    """
    Base model adding common fields (standard among this project).
    """
    class Meta:
        abstract = True
