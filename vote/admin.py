from vote.models import Track, Vote, ManualVote, Play, Block
from django.contrib import admin

class VoteAdmin(admin.ModelAdmin):
    list_display=('screen_name', 'track')

class TrackAdmin(admin.ModelAdmin):
    list_display=('id3_title', 'id3_artist')

class ManualVoteAdmin(admin.ModelAdmin):
    list_display=('name', 'message', 'track', 'date')

class PlayAdmin(admin.ModelAdmin):
    list_display=('track', 'datetime')

class BlockAdmin(admin.ModelAdmin):
    list_display=('reason', 'date')

admin.site.register(Track, TrackAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(ManualVote, ManualVoteAdmin)
admin.site.register(Play, PlayAdmin)
admin.site.register(Block, BlockAdmin)
