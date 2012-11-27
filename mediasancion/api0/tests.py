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

from restsources.restponders.json_util import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from mediasancion.core.models import Partido, Distrito


class DistritosTest(TestCase):
    fixtures = 'api0_test',

    def test_list(self):
        """GET api0:core:distritos:list"""
        url = reverse('api0:core:distritos:list')
        self.assertEquals(url, "/api/0/core/distritos/")

        resp = self.client.get(url, HTTP_ACCEPT='application/json')
        r = json.loads(resp.content)

        # Example content:
        # {
        #   "status": "OK",
        #   "payload": {
        #     "distritos": [
        #       {
        #         "distrito": {
        #           "url": "/api/0/core/distritos/48a1168c-eb0b-4606-b496-2c8f00b07de5/",
        #           "uuid": "48a1168c-eb0b-4606-b496-2c8f00b07de5"
        #         }
        #       },
        #       {
        #         "distrito": {
        #           "url": "/api/0/core/distritos/7aa3504c-0376-48b6-9e90-037003c4f267/",
        #           "uuid": "7aa3504c-0376-48b6-9e90-037003c4f267"
        #         }
        #       }
        #     ]
        #   }
        # }

        self.assertEquals(r['status'], 'OK')
        self.assertEquals(r['payload'].keys(), ['distritos'])

        distritos = r['payload']['distritos']
        self.assertTrue(isinstance(distritos, list))
        self.assertEquals(len(distritos), 2)

        for x in distritos:
            self.assertEquals(x.keys(), ['distrito'])
            distrito = x['distrito']

            self.assertEquals(sorted(distrito.keys()), ['url', 'uuid'])
            self.assertEquals(distrito['url'], reverse('api0:core:distritos:detail', kwargs={'uuid': distrito['uuid']}))

    def test_detail(self):
        """GET api0:core:distritos:detail"""
        url = reverse('api0:core:distritos:detail', kwargs={'uuid': '48a1168c-eb0b-4606-b496-2c8f00b07de5'})
        self.assertEquals(url, "/api/0/core/distritos/48a1168c-eb0b-4606-b496-2c8f00b07de5/")

        resp = self.client.get(url, HTTP_ACCEPT='application/json')
        r = json.loads(resp.content)

        # Example content:
        # {
        #   "status": "OK",
        #   "payload": {
        #     "distrito": {
        #       "legisladores": [
        #         {
        #           "legislador": {
        #             "url": "/api/0/congreso/diputados/legisladores/a6b5c2a6-4027-4f99-8221-b2470ae7987a/",
        #             "uuid": "a6b5c2a6-4027-4f99-8221-b2470ae7987a"
        #           }
        #         }
        #       ],
        #       "uuid": "48a1168c-eb0b-4606-b496-2c8f00b07de5",
        #       "url": "/api/0/core/distritos/48a1168c-eb0b-4606-b496-2c8f00b07de5/",
        #       "remote_id": "",
        #       "remote_source": "",
        #       "nombre": "distrito1",
        #       "remote_url": ""
        #     }
        #   }
        # }

        self.assertEquals(r['status'], 'OK')
        self.assertEquals(r['payload'].keys(), ['distrito'])

        distrito = r['payload']['distrito']
        self.assertEquals(sorted(distrito.keys()), ['legisladores','nombre', 'remote_id',
                                                    'remote_source', 'remote_url', 'url', 'uuid'])
        self.assertEquals(distrito['url'], reverse('api0:core:distritos:detail', kwargs={'uuid': distrito['uuid']}))
        self.assertEquals(distrito['uuid'], '48a1168c-eb0b-4606-b496-2c8f00b07de5')
        self.assertEquals(distrito['nombre'], 'distrito1')

        legislador = distrito['legisladores'][0]['legislador']
        self.assertTrue(Distrito.objects.get(uuid='48a1168c-eb0b-4606-b496-2c8f00b07de5').legislador_set.get(uuid=legislador['uuid']))


class PartidosPoliticosTest(TestCase):
    fixtures = 'api0_test',

    def test_list(self):
        """GET api0:core:partidos:list"""
        url = reverse('api0:core:partidos:list')
        self.assertEquals(url, "/api/0/core/partidos/")

        resp = self.client.get(url, HTTP_ACCEPT='application/json')
        r = json.loads(resp.content)

        # Example content:
        # {
        #   "status": "OK",
        #   "payload": {
        #     "partidos": [
        #       {
        #         "partido": {
        #           "url": "/api/0/core/partidos/0bb6585f-3d9b-49df-8a80-6c93bdeece75/",
        #           "uuid": "0bb6585f-3d9b-49df-8a80-6c93bdeece75"
        #         }
        #       },
        #       {
        #         "partido": {
        #           "url": "/api/0/core/partidos/0b841907-b3f8-42b2-8a35-fd30c865f2af/",
        #           "uuid": "0b841907-b3f8-42b2-8a35-fd30c865f2af"
        #         }
        #       }
        #     ]
        #   }
        # }

        self.assertEquals(r['status'], 'OK')
        self.assertEquals(r['payload'].keys(), ['partidos'])

        partidos = r['payload']['partidos']
        self.assertTrue(isinstance(partidos, list))
        self.assertEquals(len(partidos), 2)

        for x in partidos:
            self.assertEquals(x.keys(), ['partido'])
            partido = x['partido']

            self.assertEquals(sorted(partido.keys()), ['url', 'uuid'])
            self.assertEquals(partido['url'], reverse('api0:core:partidos:detail', kwargs={'uuid': partido['uuid']}))

    def test_detail(self):
        """GET api0:core:partidos:detail"""
        url = reverse('api0:core:partidos:detail', kwargs={'uuid': '0bb6585f-3d9b-49df-8a80-6c93bdeece75'})
        self.assertEquals(url, "/api/0/core/partidos/0bb6585f-3d9b-49df-8a80-6c93bdeece75/")

        resp = self.client.get(url, HTTP_ACCEPT='application/json')
        r = json.loads(resp.content)

        # Example content:
        # {
        #   "status": "OK",
        #   "payload": {
        #     "partido": {
        #       "legisladores": [
        #         {
        #           "legislador": {
        #             "url": "/api/0/congreso/diputados/legisladores/a6b5c2a6-4027-4f99-8221-b2470ae7987a/",
        #             "uuid": "a6b5c2a6-4027-4f99-8221-b2470ae7987a"
        #           }
        #         },
        #         {
        #           "legislador": {
        #             "url": "/api/0/congreso/diputados/legisladores/aef2f84f-0d2e-4303-83d1-797e934be93d/",
        #             "uuid": "aef2f84f-0d2e-4303-83d1-797e934be93d"
        #           }
        #         }
        #       ],
        #       "uuid": "0bb6585f-3d9b-49df-8a80-6c93bdeece75",
        #       "url": "/api/0/core/partidos/0bb6585f-3d9b-49df-8a80-6c93bdeece75/",
        #       "remote_id": "",
        #       "remote_source": "",
        #       "nombre": "partido1",
        #       "remote_url": ""
        #     }
        #   }
        # }

        self.assertEquals(r['status'], 'OK')
        self.assertEquals(r['payload'].keys(), ['partido'])

        partido = r['payload']['partido']
        self.assertEquals(sorted(partido.keys()), ['legisladores','nombre', 'remote_id',
                                                    'remote_source', 'remote_url', 'url', 'uuid'])
        self.assertEquals(partido['url'], reverse('api0:core:partidos:detail', kwargs={'uuid': partido['uuid']}))
        self.assertEquals(partido['uuid'], '0bb6585f-3d9b-49df-8a80-6c93bdeece75')
        self.assertEquals(partido['nombre'], 'partido1')

        legislador = partido['legisladores'][0]['legislador']
        self.assertTrue(Partido.objects.get(uuid='0bb6585f-3d9b-49df-8a80-6c93bdeece75').legislador_set.get(uuid=legislador['uuid']))
