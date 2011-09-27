# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Distrito'
        db.create_table('core_distrito', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('core', ['Distrito'])

        # Adding model 'Partido'
        db.create_table('core_partido', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('core', ['Partido'])

        # Adding model 'Bloque'
        db.create_table('core_bloque', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('core', ['Bloque'])

        # Adding model 'Persona'
        db.create_table('core_persona', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('remote_source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('remote_url', self.gf('django.db.models.fields.URLField')(max_length=1023, blank=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=36, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('documento_tipo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('documento_numero', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Persona'])


    def backwards(self, orm):
        
        # Deleting model 'Distrito'
        db.delete_table('core_distrito')

        # Deleting model 'Partido'
        db.delete_table('core_partido')

        # Deleting model 'Bloque'
        db.delete_table('core_bloque')

        # Deleting model 'Persona'
        db.delete_table('core_persona')


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
            'documento_tipo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['core']
