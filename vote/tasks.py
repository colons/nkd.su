from datetime import datetime

import Levenshtein

from celery import task

from models import Play, Vote, Track, showtime

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

from sys import exc_info

def tweettime(tweet):
    try:
        tweettime = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    except ValueError:
        #Thu, 20 Sep 2012 14:51:24 +0000
        tweettime = datetime.strptime(tweet['created_at'], '%a, %d %b %Y %H:%M:%S +0000')

    return timezone.make_aware(tweettime, timezone.utc)


def strip_after_hashtags(text):
    return text.split(' #')[0]

@task
def log_play(tweet):
    text = strip_after_hashtags(tweet['text'])
    match = None
    matches = []
    tracks = Track.objects.all()

    for track in tracks:
        if track.canonical_string() in text:
            matches.append(track)

    if matches:
        match = min(matches, key=lambda t: len(t.canonical_string()))
    else:
        for track in tracks:
            leven = Levenshtein.ratio(text, track.canonical_string())
            if leven > .7:
                matches.append((leven, track))

        if matches:
            match = max(matches)[1]

    if match:
        play = Play(
                datetime=tweettime(tweet),
                track=match
                )

        try:
            play.clean()
        except ValidationError:
            print exc_info()
        else:
            play.save()

@task
def log_vote(tweet):
    # get song id
    for word in tweet['text'].split():
        try:
            track = Track.objects.get(id=int(word))
        except ValueError:
            # is not a number
            pass
        except Vote.DoesNotExist:
            # is not ours
            pass
        else:
            break
    else:
        return # no appropriate track was found

    date = tweettime(tweet)

    # make Vote
    if 'user' in tweet: # this is from the streaming api
        the_vote = Vote(
                screen_name=tweet['user']['screen_name'],
                user_id=tweet['user']['id'],
                tweet_id=tweet['id'],
                track=track,
                date=date,
                user_image=tweet['user']['profile_image_url'],
                text=tweet['text'],
                )

    else: # this is from the archive
        the_vote = Vote(
                screen_name=tweet['from_user'],
                user_id=tweet['from_user_id'],
                tweet_id=tweet['id'],
                track=track,
                date=date,
                user_image=tweet['profile_image_url'],
                text=tweet['text'],
                )

    try:
        the_vote.clean()
    except ValidationError:
        print exc_info()
    else:
        the_vote.save()

