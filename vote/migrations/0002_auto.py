# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field tracks on 'Vote'
        db.create_table('vote_vote_tracks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vote', models.ForeignKey(orm['vote.vote'], null=False)),
            ('track', models.ForeignKey(orm['vote.track'], null=False))
        ))
        db.create_unique('vote_vote_tracks', ['vote_id', 'track_id'])


    def backwards(self, orm):
        # Removing M2M table for field tracks on 'Vote'
        db.delete_table('vote_vote_tracks')


    models = {
        'vote.block': {
            'Meta': {'object_name': 'Block'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Track']"})
        },
        'vote.discard': {
            'Meta': {'object_name': 'Discard'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Track']"})
        },
        'vote.manualvote': {
            'Meta': {'object_name': 'ManualVote'},
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Track']"})
        },
        'vote.play': {
            'Meta': {'object_name': 'Play'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Track']"}),
            'tweet_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'vote.shortlist': {
            'Meta': {'object_name': 'Shortlist'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Track']"})
        },
        'vote.track': {
            'Meta': {'object_name': 'Track'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'id3_album': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'id3_artist': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id3_title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'show_en': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'show_ka': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'show_ro': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'title_ka': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'title_ro': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'vote.vote': {
            'Meta': {'object_name': 'Vote'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Track']", 'blank': 'True'}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'multi+'", 'blank': 'True', 'to': "orm['vote.Track']"}),
            'tweet_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_image': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['vote']