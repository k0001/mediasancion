# coding: utf8

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


# It's recommended that you import items in the following order:
#  1. LegisladorItem
#  2. ProyectoItem
#  3. FirmaProyecto|TramiteProyectoItem|DictamenProyectoItem

# This program is ugly as shit.



import json
import logging
import optparse
import os
import random
import re
import signal
import sys
import time
import isodate
from datetime import datetime
from pprint import pprint

from django.db.models import Q
from django.db import transaction

from mediasancion.core.models import Partido, Distrito, Bloque, Persona
from mediasancion.congreso.models import (Proyecto, FirmaProyecto, Legislador,
        Comision, DictamenProyecto, TramiteProyecto)


logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(os.path.basename(__file__))

AUDIT_ORIGIN = u'mscrap_import:%s' % datetime.utcnow().isoformat()


def store_legislador_item(x):
    try:
        distrito = Distrito.objects.get(nombre=x['distrito_nombre'])
    except Distrito.DoesNotExist:
        distrito = Distrito(nombre=x['distrito_nombre'], origin=AUDIT_ORIGIN)
        distrito.resource_source = x['resource_source']
        distrito.resource_url = x['resource_url']
        distrito.save()

    if x.get('bloque_nombre'):
        try:
            bloque = Bloque.objects.get(nombre=x['bloque_nombre'])
        except Bloque.DoesNotExist:
            bloque = Bloque(nombre=x['bloque_nombre'], origin=AUDIT_ORIGIN)
            bloque.resource_source = x['resource_source']
            bloque.resource_url = x['resource_url']
            bloque.save()
    else:
        bloque = None

    if x.get('partido_nombre'):
        try:
            partido = Partido.objects.get(nombre=x['partido_nombre'])
        except Partido.DoesNotExist:
            partido = Partido(nombre=x['partido_nombre'], origin=AUDIT_ORIGIN)
            partido.resource_source = x['resource_source']
            partido.resource_url = x['resource_url']
            partido.save()
    else:
        partido = None

    persona_created = True
    try:
        persona = Persona.objects.get(nombre=x['nombre'],
                                            apellido=x['apellido'],
                                            legislador__camara=x['camara'],
                                            legislador__bloque=bloque,
                                            legislador__distrito=distrito,
                                            legislador__inicio=isodate.parse_date(x['mandato_inicio']),
                                            legislador__fin=isodate.parse_date(x['mandato_fin']))
        persona_created = False
    except Persona.DoesNotExist:
        try:
            persona = Persona.objects.get(nombre=x['nombre'], apellido=x['apellido'])
            persona_created = False
        except Persona.MultipleObjectsReturned:
            log.error((u"This is an expected error! Aparently you have more than one Persona named: "
                       u"%(apellido)s, %(nombre)s. You'll have to fix this by hand. Set var 'persona' "
                       u"to the desired Persona instance and continue (c)") % x)
            import ipdb; ipdb.set_trace()
        except Persona.DoesNotExist:
            persona = Persona(nombre=x['nombre'], apellido=x['apellido'], origin=AUDIT_ORIGIN)

        try:
            assert isinstance(persona, Persona)
        except (NameError, AssertionError):
            raise RuntimeError(u"Missing Persona, sorry, need to abort.")

    persona.email = x.get('email') or None # the 'or None' thing is cuz we don't want empty strings.
    persona.telefono = x.get('telefono') or None
    persona.foto = x.get('foto_url') or None # <--- makes no sense, but we don't care right now.
    persona.save()

    if persona_created:
        persona.resource_source = x['resource_source']
        persona.resource_url = x['resource_url']
        persona.resource_id = x['resource_id']
        persona.save()
        log.debug(u'Created %s Persona' % persona.uuid)
    else:
        log.debug(u'Updated %s Persona' % persona.uuid)

    try:
        legislador = Legislador.objects.get(persona=persona,
                                      camara=x['camara'],
                                      bloque=bloque,
                                      distrito=distrito,
                                      inicio=isodate.parse_date(x['mandato_inicio']),
                                      fin=isodate.parse_date(x['mandato_fin']))
        log.debug(u'Updated %s Legislador' % legislador.uuid)
    except Legislador.DoesNotExist:
        legislador = Legislador(persona=persona,
                          camara=x['camara'],
                          bloque=bloque,
                          partido=partido,
                          distrito=distrito,
                          inicio=isodate.parse_date(x['mandato_inicio']),
                          fin=isodate.parse_date(x['mandato_fin']))
        legislador.resource_source = x['resource_source']
        legislador.resource_url = x['resource_url']
        legislador.resource_id = x['resource_id']
        legislador.origin = AUDIT_ORIGIN
        legislador.save()
        log.debug(u'Created %s Legislador' % legislador.uuid)

    return True

def store_proyecto_item(x):
    try:
        p = Proyecto.objects.get(camara_origen_expediente=x['camara_origen_expediente'],
                                 camara_origen=x['camara_origen'])
        proyecto_created = False
    except Proyecto.DoesNotExist:
        p = Proyecto(camara_origen_expediente=x['camara_origen_expediente'],
                     camara_origen=x['camara_origen'],
                     origin=AUDIT_ORIGIN)
        proyecto_created = True

    p.resource_source = x['resource_source']
    p.resource_url = x['resource_url']
    p.resource_id = x['resource_id']

    p.origen = x['origen']

    p.camara_revisora = x['camara_revisora'] if 'camara_revisora' in x else None
    p.camara_revisora_expediente = x.get('camara_revisora_expediente') or ''

    p.reproduccion_expediente = x.get('reproduccion_expediente') or ''

    p.ley_numero = x.get('ley_numero')

    p.tipo = x['tipo']
    p.mensaje = x.get('mensaje_codigo') or ''

    p.publicacion_en = x.get('publicacion_en') or ''
    p.publicacion_fecha = isodate.parse_date(x['publicacion_fecha'])

    p.texto_completo_url = x.get('texto_completo_url', '')
    p.texto_mediasancion_senadores_url = x.get('texto_mediasancion_senadores_url', '')
    p.texto_mediasancion_diputados_url = x.get('texto_mediasancion_diputados_url', '')

    p.sumario = x['sumario']

    p.save()

    cd = x.get('comisiones_diputados', ())


    for s in cd:
        s = s.capitalize()
        try:
            c = Comision.objects.get(camara='D', nombre__iexact=s)
        except Comision.DoesNotExist:
            c = Comision(camara='D', nombre=s, origin=AUDIT_ORIGIN)
            c.resource_source = x['resource_source']
            c.resource_url = x['resource_url']
            c.save()
        if not c in p.comisiones.all():
            p.comisiones.add(c)

    for s in x.get('comisiones_senadores', ()):
        s = s.capitalize()
        try:
            c = Comision.objects.get(camara='S', nombre__iexact=s)
        except Comision.DoesNotExist:
            c = Comision(camara='S', nombre=s, origin=AUDIT_ORIGIN)
            c.resource_source = x['resource_source']
            c.resource_url = x['resource_url']
            c.save()
        if not c in p.comisiones.all():
            p.comisiones.add(c)

    if proyecto_created:
        log.debug(u'Created %s Proyecto' % p.uuid)
        return True
    else:
        log.debug(u'Updated %s Proyecto' % p.uuid)
        return True



def store_firmaproyecto_item(x):
    try:
        proyecto = Proyecto.objects.get(camara_origen_expediente=x['proyecto_camara_origen_expediente'],
                                        camara_origen=x['proyecto_camara_origen'])
    except Proyecto.DoesNotExist:
        return False

    if x.get('firmante_bloque'):
        try:
            bloque = Bloque.objects.get(nombre=x['firmante_bloque'])
        except Bloque.DoesNotExist:
            bloque = Bloque(nombre=x['firmante_bloque'], origin=AUDIT_ORIGIN)
            bloque.resource_source = x['resource_source']
            bloque.resource_url = x['resource_url']
            bloque.save()
    else:
        bloque = None

    if x.get('firmante_distrito'):
        try:
            distrito = Distrito.objects.get(nombre=x['firmante_distrito'])
        except Distrito.DoesNotExist:
            distrito = Distrito(nombre=x['firmante_distrito'], origin=AUDIT_ORIGIN)
            distrito.resource_source = x['resource_source']
            distrito.resource_url = x['resource_url']
            distrito.save()
    else:
        distrito = None

    poder =x['firmante_poder']

    firmante_special = x.get('firmante_special') or u''

    if not firmante_special:
        firmante_apellido = x.get('firmante_apellido') or u''
        firmante_nombre = x.get('firmante_nombre') or u''

        try:
            persona = Persona.objects.get(apellido=firmante_apellido,
                                                nombre=firmante_nombre)
        except Persona.DoesNotExist:
            persona = Persona(apellido=firmante_apellido,
                                    nombre=firmante_nombre,
                                    origin=AUDIT_ORIGIN)
            persona.resource_source = x['resource_source']
            persona.resource_url = x['resource_url']
            persona.save()

        try:
            legislador = Legislador.objects.get(persona=persona,
                                                bloque=bloque,
                                                distrito=distrito)
        except Legislador.DoesNotExist:
            # if legislador created, inicio and fin will be missing. Whatever.
            legislador = Legislador(persona=persona,
                              bloque=bloque,
                              distrito=distrito,
                              camara='?',
                              origin=AUDIT_ORIGIN)
            legislador.resource_source = x['resource_source']
            legislador.resource_url = x['resource_url']
            legislador.save()
    else:
        persona = legislador = None

    try:
        fp = FirmaProyecto.objects.get(proyecto=proyecto,
                                       legislador=legislador,
                                       poder=poder,
                                       poder_who=firmante_special,
                                       tipo_firma=x['tipo_firma'])
        log.debug(u'Updated %s FirmaProyecto' % fp.uuid)
    except FirmaProyecto.DoesNotExist:
        fp = FirmaProyecto(proyecto=proyecto,
                           legislador=legislador,
                           poder=poder,
                           poder_who=firmante_special,
                           tipo_firma=x['tipo_firma'],
                           origin=AUDIT_ORIGIN)
        fp.resource_source = x['resource_source']
        fp.resource_url = x['resource_url']
        fp.resource_id = x.get('resource_id')
        fp.save()
        log.debug(u'Created %s FirmaProyecto' % fp.uuid)

    return True


def store_dictamenproyecto_item(x):
    try:
        proyecto = Proyecto.objects.get(camara_origen_expediente=x['proyecto_camara_origen_expediente'],
                                        camara_origen=x['proyecto_camara_origen'])
    except Proyecto.DoesNotExist:
        return False

    x_fecha = isodate.parse_date(x['fecha']) if 'fecha' in x else None

    try:
        dp = DictamenProyecto.objects.get(proyecto=proyecto,
                                          camara=x['camara'],
                                          index=int(x['index']))
    except DictamenProyecto.DoesNotExist:
        dp = DictamenProyecto(proyecto=proyecto,
                              camara=x['camara'],
                              index=int(x['index']),
                              fecha=x_fecha,
                              orden_del_dia=(x.get('orden_del_dia') or u''),
                              descripcion=(x.get('descripcion') or u''),
                              resultado=(x.get('resultado') or u''),
                              origin=AUDIT_ORIGIN)
        dp.resource_source = x['resource_source']
        dp.resource_url = x['resource_url']
        dp.resource_id = x.get('resource_id')
        dp.save()
        log.debug(u'Created %s DictamenProyecto' % dp.uuid)

    else:
        dp_changed = False
        if dp.resultado and x.get('resultado') and dp.resultado != x.get('resultado'):
            dp.resultado = x.get('resultado', u'')
            dp_changed = True
        if dp.descripcion and x.get('descripcion') and dp.descripcion != x.get('descripcion'):
            dp.descripcion = x.get('descripcion', u'')
            dp_changed = True

        if dp_changed:
            dp.save()
        log.debug(u'Updated %s DictamenProyecto' % dp.uuid)

    return True


def store_tramiteproyecto_item(x):
    try:
        proyecto = Proyecto.objects.get(camara_origen_expediente=x['proyecto_camara_origen_expediente'],
                                        camara_origen=x['proyecto_camara_origen'])
    except Proyecto.DoesNotExist:
        return False

    x_fecha = isodate.parse_date(x['fecha']) if 'fecha' in x else None

    try:
        tp = TramiteProyecto.objects.get(proyecto=proyecto,
                                         camara=x['camara'],
                                         index=int(x['index']))
    except TramiteProyecto.DoesNotExist:
        tp = TramiteProyecto(proyecto=proyecto,
                             camara=x['camara'],
                             index=int(x['index']),
                             fecha=x_fecha,
                             descripcion=(x.get('descripcion') or u''),
                             resultado=(x.get('resultado') or u''),
                             origin=AUDIT_ORIGIN)
        tp.resource_source = x['resource_source']
        tp.resource_url = x['resource_url']
        tp.resource_id = x.get('resource_id')
        tp.save()
        log.debug(u'Created %s TramiteProyecto' % tp.uuid)

    else:
        tp_changed = False
        if tp.resultado and x.get('resultado') and tp.resultado != x.get('resultado'):
            tp.resultado = x.get('resultado', u'')
            tp_changed = True
        if tp.descripcion and x.get('descripcion') and tp.descripcion != x.get('descripcion'):
            tp.descripcion = x.get('descripcion', u'')
            tp_changed = True

        if tp_changed:
            tp.save()
        log.debug(u'Updated %s TramiteProyecto' % tp.uuid)

    return True



@transaction.commit_manually
def store_item(t, x):
    ts = { 'LegisladorItem': store_legislador_item,
           'ProyectoItem': store_proyecto_item,
           'FirmaProyectoItem': store_firmaproyecto_item,
           'DictamenProyectoItem': store_dictamenproyecto_item,
           'TramiteProyectoItem': store_tramiteproyecto_item }
    try:
        _store = ts[t]
    except KeyError:
        log.warning(u"Skiping %s" % t)
        return

    try:
        s = _store(x)
    except:
        transaction.rollback()
        raise

    if s:
        transaction.commit()
        return True
    else:
        log.debug(u"Couldn't store %s" % t)
        transaction.rollback()
        return False


def store_raw(line):
    t, x = json.loads(line)
    return store_item(t, x)

def main_store(lines):
    log.info('Storing...')
    for line in lines:
        if not store_raw(line):
            return



def _sighandle_pdb(sig, frame):
    import pdb
    pdb.Pdb().set_trace(frame)
signal.signal(signal.SIGUSR1, _sighandle_pdb)


def parse_args():
    parser = optparse.OptionParser(usage=u"usage: %prog [options] FILE [FILE..]")

    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose',
                      help=u"verbose output")
    parser.add_option('--debug',
                      action='store_true', dest='debug',
                      help=u"debug output")
    parser.add_option('--wtf',
                      action='store_true', dest='wtf',
                      help=u"enable WTF post-mortem debugger")

    opts, args = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    return opts, args


if __name__ == '__main__':
    opts, args = parse_args()

    if opts.debug:
        log.setLevel(logging.DEBUG)
    elif opts.verbose:
        log.setLevel(logging.INFO)

    log.info('PID: %d' % os.getpid())
    log.info('SIGUSR1: Start debugger.')
    log.info('SIGUSR2: Print status.')

    if opts.wtf:
        log.info(u"WTF Post-mortem debugger enabled")
    try:
        for fname in args:
            with open(fname, 'rb') as f: # we use ascii-only input (JSON)
                log.info(u"Opening %s..." % fname)
                main_store(f)
    except Exception:
        log.error(u"Something bad happened!!! Nothing will saved.")
        if opts.wtf:
            from wtf import WTF
            WTF()
        else:
            raise
