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

import unicodedata

from haystack.indexes import *
from haystack import indexes

from ..utils.templatetags.utils_unicode import normalize_unicode


class StandardSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)

    def prepare_text(self, obj):
        # We are OK using NFKD, since our texts are in spanish :)
        return unicodedata.normalize('NFKD', self.prepared_data['text']) \
                    .encode('ascii', 'ignore').decode('ascii')

