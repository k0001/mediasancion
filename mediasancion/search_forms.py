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

import unicodedata

from django import forms

from haystack.forms import SearchForm

from mediasancion.congreso.models import Proyecto


class MSSearchForm(SearchForm):
    proyecto_tipo = forms.MultipleChoiceField(choices=Proyecto.TIPO_CHOICES,
                                              required=False)

    def clean_q(self):
        data = self.cleaned_data.get('q')
        if data is not None:
            return data.strip()

    @property
    def q_nfkd(self):
        # We are OK using NFKD, since our texts are in spanish :)
        return unicodedata.normalize('NFKD', self.cleaned_data['q']) \
                    .encode('ascii', 'ignore').decode('ascii')

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.q_nfkd).order_by('-pub_date')

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

