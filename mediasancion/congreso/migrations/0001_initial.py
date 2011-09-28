# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Comision'
        db.create_table('congreso_comision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('camara', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('congreso', ['Comision'])

        # Adding unique constraint on 'Comision', fields ['camara', 'nombre']
        db.create_unique('congreso_comision', ['camara', 'nombre'])

        # Adding model 'Legislador'
        db.create_table('congreso_legislador', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Persona'], null=True)),
            ('camara', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('inicio', self.gf('django.db.models.fields.DateField')(null=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True)),
            ('partido', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Partido'], null=True)),
            ('bloque', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Bloque'], null=True)),
            ('distrito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Distrito'], null=True)),
        ))
        db.send_create_signal('congreso', ['Legislador'])

        # Adding model 'MembresiaComision'
        db.create_table('congreso_membresiacomision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('legislador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['congreso.Legislador'], null=True)),
            ('comision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['congreso.Comision'])),
            ('cargo', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('congreso', ['MembresiaComision'])

        # Adding model 'Reunion'
        db.create_table('congreso_reunion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('camara', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('nro_periodo', self.gf('django.db.models.fields.IntegerField')()),
            ('nro_reunion', self.gf('django.db.models.fields.IntegerField')()),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('congreso', ['Reunion'])

        # Adding model 'AsistenciaReunion'
        db.create_table('congreso_asistenciareunion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('reunion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['congreso.Reunion'])),
            ('legislador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['congreso.Legislador'], null=True)),
            ('asistencia', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('congreso', ['AsistenciaReunion'])

        # Adding model 'Proyecto'
        db.create_table('congreso_proyecto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('origen', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('camara_origen', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('camara_origen_expediente', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('camara_revisora', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('camara_revisora_expediente', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('tipo_verbose', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mensaje', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('sumario', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fundamentos', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('texto_completo_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('texto_mediasancion_senadores_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('texto_mediasancion_diputados_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('publicacion_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('publicacion_fecha', self.gf('django.db.models.fields.DateField')()),
            ('reproduccion_expediente', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('ley_numero', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('congreso', ['Proyecto'])

        # Adding unique constraint on 'Proyecto', fields ['camara_origen', 'camara_origen_expediente']
        db.create_unique('congreso_proyecto', ['camara_origen', 'camara_origen_expediente'])

        # Adding M2M table for field comisiones on 'Proyecto'
        db.create_table('congreso_proyecto_comisiones', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proyecto', models.ForeignKey(orm['congreso.proyecto'], null=False)),
            ('comision', models.ForeignKey(orm['congreso.comision'], null=False))
        ))
        db.create_unique('congreso_proyecto_comisiones', ['proyecto_id', 'comision_id'])

        # Adding model 'FirmaProyecto'
        db.create_table('congreso_firmaproyecto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('poder', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('legislador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['congreso.Legislador'], null=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['congreso.Proyecto'])),
            ('tipo_firma', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('poder_who', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('congreso', ['FirmaProyecto'])

        # Adding unique constraint on 'FirmaProyecto', fields ['legislador', 'proyecto']
        db.create_unique('congreso_firmaproyecto', ['legislador_id', 'proyecto_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FirmaProyecto', fields ['legislador', 'proyecto']
        db.delete_unique('congreso_firmaproyecto', ['legislador_id', 'proyecto_id'])

        # Removing unique constraint on 'Proyecto', fields ['camara_origen', 'camara_origen_expediente']
        db.delete_unique('congreso_proyecto', ['camara_origen', 'camara_origen_expediente'])

        # Removing unique constraint on 'Comision', fields ['camara', 'nombre']
        db.delete_unique('congreso_comision', ['camara', 'nombre'])

        # Deleting model 'Comision'
        db.delete_table('congreso_comision')

        # Deleting model 'Legislador'
        db.delete_table('congreso_legislador')

        # Deleting model 'MembresiaComision'
        db.delete_table('congreso_membresiacomision')

        # Deleting model 'Reunion'
        db.delete_table('congreso_reunion')

        # Deleting model 'AsistenciaReunion'
        db.delete_table('congreso_asistenciareunion')

        # Deleting model 'Proyecto'
        db.delete_table('congreso_proyecto')

        # Removing M2M table for field comisiones on 'Proyecto'
        db.delete_table('congreso_proyecto_comisiones')

        # Deleting model 'FirmaProyecto'
        db.delete_table('congreso_firmaproyecto')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'congreso.asistenciareunion': {
            'Meta': {'object_name': 'AsistenciaReunion'},
            'asistencia': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['congreso.Legislador']", 'null': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'reunion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['congreso.Reunion']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'congreso.comision': {
            'Meta': {'unique_together': "(('camara', 'nombre'),)", 'object_name': 'Comision'},
            'camara': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'congreso.firmaproyecto': {
            'Meta': {'unique_together': "(('legislador', 'proyecto'),)", 'object_name': 'FirmaProyecto'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['congreso.Legislador']", 'null': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'poder': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'poder_who': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['congreso.Proyecto']"}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'tipo_firma': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'congreso.legislador': {
            'Meta': {'ordering': "('-fin', '-inicio')", 'object_name': 'Legislador'},
            'bloque': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Bloque']", 'null': 'True'}),
            'camara': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Distrito']", 'null': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'partido': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Partido']", 'null': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Persona']", 'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'congreso.membresiacomision': {
            'Meta': {'object_name': 'MembresiaComision'},
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'comision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['congreso.Comision']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['congreso.Legislador']", 'null': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'congreso.proyecto': {
            'Meta': {'unique_together': "(('camara_origen', 'camara_origen_expediente'),)", 'object_name': 'Proyecto'},
            'camara_origen': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'camara_origen_expediente': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'camara_revisora': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'camara_revisora_expediente': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'comisiones': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['congreso.Comision']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'firmantes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['congreso.Legislador']", 'through': "orm['congreso.FirmaProyecto']", 'symmetrical': 'False'}),
            'fundamentos': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ley_numero': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mensaje': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'origen': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'publicacion_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publicacion_fecha': ('django.db.models.fields.DateField', [], {}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'reproduccion_expediente': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'sumario': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'texto_completo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'texto_mediasancion_diputados_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'texto_mediasancion_senadores_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'tipo_verbose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'congreso.reunion': {
            'Meta': {'object_name': 'Reunion'},
            'camara': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nro_periodo': ('django.db.models.fields.IntegerField', [], {}),
            'nro_reunion': ('django.db.models.fields.IntegerField', [], {}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.bloque': {
            'Meta': {'object_name': 'Bloque'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'core.distrito': {
            'Meta': {'object_name': 'Distrito'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'core.partido': {
            'Meta': {'object_name': 'Partido'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'core.persona': {
            'Meta': {'object_name': 'Persona'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'documento_numero': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'documento_tipo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.URLField', [], {'max_length': '1023', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['congreso']
