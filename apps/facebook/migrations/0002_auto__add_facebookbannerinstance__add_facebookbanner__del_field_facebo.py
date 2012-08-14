# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FacebookBannerInstance'
        db.create_table('facebook_facebookbannerinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['facebook.FacebookUser'])),
            ('banner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['facebook.FacebookBanner'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('can_be_an_ad', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('total_clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('leaderboard_position', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('facebook', ['FacebookBannerInstance'])

        # Adding model 'FacebookBanner'
        db.create_table('facebook_facebookbanner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('locale', self.gf('shared.models.LocaleField')(default='en-US', max_length=32)),
        ))
        db.send_create_signal('facebook', ['FacebookBanner'])

        # Deleting field 'FacebookUser.user_id'
        db.delete_column('facebook_facebookuser', 'user_id')

        # Adding field 'FacebookUser.id'
        db.add_column('facebook_facebookuser', 'id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, primary_key=True),
                      keep_default=False)

    def backwards(self, orm):
        # User chose to not deal with backwards NULL issues for 'FacebookUser.user_id'
        raise RuntimeError("Cannot reverse this migration. 'FacebookUser.user_id' and its values cannot be restored.")

        # Deleting model 'FacebookBannerInstance'
        db.delete_table('facebook_facebookbannerinstance')

        # Deleting model 'FacebookBanner'
        db.delete_table('facebook_facebookbanner')

        # Deleting field 'FacebookUser.id'
        db.delete_column('facebook_facebookuser', 'id')

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
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        'facebook.facebookbanner': {
            'Meta': {'object_name': 'FacebookBanner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'locale': ('shared.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        'facebook.facebookbannerinstance': {
            'Meta': {'object_name': 'FacebookBannerInstance'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facebook.FacebookBanner']"}),
            'can_be_an_ad': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaderboard_position': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'total_clicks': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facebook.FacebookUser']"})
        },
        'facebook.facebookuser': {
            'Meta': {'object_name': 'FacebookUser'},
            'affiliates_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'primary_key': 'True'})
        }
    }

    complete_apps = ['facebook']
