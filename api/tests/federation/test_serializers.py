import arrow

from django.urls import reverse
from django.core.paginator import Paginator

from funkwhale_api.federation import actors
from funkwhale_api.federation import keys
from funkwhale_api.federation import models
from funkwhale_api.federation import serializers
from funkwhale_api.federation import utils


def test_actor_serializer_from_ap(db):
    payload = {
        'id': 'https://test.federation/user',
        'type': 'Person',
        'following': 'https://test.federation/user/following',
        'followers': 'https://test.federation/user/followers',
        'inbox': 'https://test.federation/user/inbox',
        'outbox': 'https://test.federation/user/outbox',
        'preferredUsername': 'user',
        'name': 'Real User',
        'summary': 'Hello world',
        'url': 'https://test.federation/@user',
        'manuallyApprovesFollowers': False,
        'publicKey': {
            'id': 'https://test.federation/user#main-key',
            'owner': 'https://test.federation/user',
            'publicKeyPem': 'yolo'
        },
        'endpoints': {
            'sharedInbox': 'https://test.federation/inbox'
        },
    }

    serializer = serializers.ActorSerializer(data=payload)
    assert serializer.is_valid()

    actor = serializer.build()

    assert actor.url == payload['id']
    assert actor.inbox_url == payload['inbox']
    assert actor.outbox_url == payload['outbox']
    assert actor.shared_inbox_url == payload['endpoints']['sharedInbox']
    assert actor.followers_url == payload['followers']
    assert actor.following_url == payload['following']
    assert actor.public_key == payload['publicKey']['publicKeyPem']
    assert actor.preferred_username == payload['preferredUsername']
    assert actor.name == payload['name']
    assert actor.domain == 'test.federation'
    assert actor.summary == payload['summary']
    assert actor.type == 'Person'
    assert actor.manually_approves_followers == payload['manuallyApprovesFollowers']


def test_actor_serializer_only_mandatory_field_from_ap(db):
    payload = {
        'id': 'https://test.federation/user',
        'type': 'Person',
        'following': 'https://test.federation/user/following',
        'followers': 'https://test.federation/user/followers',
        'inbox': 'https://test.federation/user/inbox',
        'outbox': 'https://test.federation/user/outbox',
        'preferredUsername': 'user',
    }

    serializer = serializers.ActorSerializer(data=payload)
    assert serializer.is_valid()

    actor = serializer.build()

    assert actor.url == payload['id']
    assert actor.inbox_url == payload['inbox']
    assert actor.outbox_url == payload['outbox']
    assert actor.followers_url == payload['followers']
    assert actor.following_url == payload['following']
    assert actor.preferred_username == payload['preferredUsername']
    assert actor.domain == 'test.federation'
    assert actor.type == 'Person'
    assert actor.manually_approves_followers is None


def test_actor_serializer_to_ap():
    expected = {
        '@context': [
            'https://www.w3.org/ns/activitystreams',
            'https://w3id.org/security/v1',
            {},
        ],
        'id': 'https://test.federation/user',
        'type': 'Person',
        'following': 'https://test.federation/user/following',
        'followers': 'https://test.federation/user/followers',
        'inbox': 'https://test.federation/user/inbox',
        'outbox': 'https://test.federation/user/outbox',
        'preferredUsername': 'user',
        'name': 'Real User',
        'summary': 'Hello world',
        'manuallyApprovesFollowers': False,
        'publicKey': {
            'id': 'https://test.federation/user#main-key',
            'owner': 'https://test.federation/user',
            'publicKeyPem': 'yolo'
        },
        'endpoints': {
            'sharedInbox': 'https://test.federation/inbox'
        },
    }
    ac = models.Actor(
        url=expected['id'],
        inbox_url=expected['inbox'],
        outbox_url=expected['outbox'],
        shared_inbox_url=expected['endpoints']['sharedInbox'],
        followers_url=expected['followers'],
        following_url=expected['following'],
        public_key=expected['publicKey']['publicKeyPem'],
        preferred_username=expected['preferredUsername'],
        name=expected['name'],
        domain='test.federation',
        summary=expected['summary'],
        type='Person',
        manually_approves_followers=False,

    )
    serializer = serializers.ActorSerializer(ac)

    assert serializer.data == expected


def test_webfinger_serializer():
    expected = {
        'subject': 'acct:service@test.federation',
        'links': [
            {
                'rel': 'self',
                'href': 'https://test.federation/federation/instance/actor',
                'type': 'application/activity+json',
            }
        ],
        'aliases': [
            'https://test.federation/federation/instance/actor',
        ]
    }
    actor = models.Actor(
        url=expected['links'][0]['href'],
        preferred_username='service',
        domain='test.federation',
    )
    serializer = serializers.ActorWebfingerSerializer(actor)

    assert serializer.data == expected


def test_follow_serializer_to_ap(factories):
    follow = factories['federation.Follow'](local=True)
    serializer = serializers.FollowSerializer(follow)

    expected = {
        '@context': [
            'https://www.w3.org/ns/activitystreams',
            'https://w3id.org/security/v1',
            {},
        ],
        'id': follow.get_federation_url(),
        'type': 'Follow',
        'actor': follow.actor.url,
        'object': follow.target.url,
    }

    assert serializer.data == expected


def test_paginated_collection_serializer(factories):
    tfs = factories['music.TrackFile'].create_batch(size=5)
    actor = factories['federation.Actor'](local=True)

    conf = {
        'id': 'https://test.federation/test',
        'items': tfs,
        'item_serializer': serializers.AudioSerializer,
        'actor': actor,
        'page_size': 2,
    }
    expected = {
        '@context': [
            'https://www.w3.org/ns/activitystreams',
            'https://w3id.org/security/v1',
            {},
        ],
        'type': 'Collection',
        'id': conf['id'],
        'actor': actor.url,
        'totalItems': len(tfs),
        'current': conf['id'] + '?page=1',
        'last': conf['id'] + '?page=3',
        'first': conf['id'] + '?page=1',
    }

    serializer = serializers.PaginatedCollectionSerializer(conf)

    assert serializer.data == expected


def test_collection_page_serializer(factories):
    tfs = factories['music.TrackFile'].create_batch(size=5)
    actor = factories['federation.Actor'](local=True)

    conf = {
        'id': 'https://test.federation/test',
        'item_serializer': serializers.AudioSerializer,
        'actor': actor,
        'page': Paginator(tfs, 2).page(2),
    }
    expected = {
        '@context': [
            'https://www.w3.org/ns/activitystreams',
            'https://w3id.org/security/v1',
            {},
        ],
        'type': 'CollectionPage',
        'id': conf['id'] + '?page=2',
        'actor': actor.url,
        'totalItems': len(tfs),
        'partOf': conf['id'],
        'prev': conf['id'] + '?page=1',
        'next': conf['id'] + '?page=3',
        'first': conf['id'] + '?page=1',
        'last': conf['id'] + '?page=3',
        'items': [
            conf['item_serializer'](
                i,
                context={'actor': actor, 'include_ap_context': False}
            ).data
            for i in conf['page'].object_list
        ]
    }

    serializer = serializers.CollectionPageSerializer(conf)

    assert serializer.data == expected


def test_activity_pub_audio_serializer_to_library_track(factories):
    remote_library = factories['federation.Library']()
    audio = factories['federation.Audio']()
    serializer = serializers.AudioSerializer(
        data=audio, context={'library': remote_library})

    assert serializer.is_valid(raise_exception=True)

    lt = serializer.save()

    assert lt.pk is not None
    assert lt.url == audio['id']
    assert lt.library == remote_library
    assert lt.audio_url == audio['url']['href']
    assert lt.audio_mimetype == audio['url']['mediaType']
    assert lt.metadata == audio['metadata']
    assert lt.title == audio['metadata']['recording']['title']
    assert lt.artist_name == audio['metadata']['artist']['name']
    assert lt.album_title == audio['metadata']['release']['title']
    assert lt.published_date == arrow.get(audio['published'])


def test_activity_pub_audio_serializer_to_ap(factories):
    tf = factories['music.TrackFile'](mimetype='audio/mp3')
    library = actors.SYSTEM_ACTORS['library'].get_actor_instance()
    expected = {
        '@context': serializers.AP_CONTEXT,
        'type': 'Audio',
        'id': tf.get_federation_url(),
        'name': tf.track.full_name,
        'published': tf.creation_date.isoformat(),
        'updated': tf.modification_date.isoformat(),
        'metadata': {
            'artist': {
                'musicbrainz_id': tf.track.artist.mbid,
                'name': tf.track.artist.name,
            },
            'release': {
                'musicbrainz_id': tf.track.album.mbid,
                'title': tf.track.album.title,
            },
            'recording': {
                'musicbrainz_id': tf.track.mbid,
                'title': tf.track.title,
            },
        },
        'url': {
            'href': utils.full_url(tf.path),
            'type': 'Link',
            'mediaType': 'audio/mp3'
        },
        'attributedTo': [
            library.url
        ]
    }

    serializer = serializers.AudioSerializer(tf, context={'actor': library})

    assert serializer.data == expected


def test_activity_pub_audio_serializer_to_ap_no_mbid(factories):
    tf = factories['music.TrackFile'](
        mimetype='audio/mp3',
        track__mbid=None,
        track__album__mbid=None,
        track__album__artist__mbid=None,
    )
    library = actors.SYSTEM_ACTORS['library'].get_actor_instance()
    expected = {
        '@context': serializers.AP_CONTEXT,
        'type': 'Audio',
        'id': tf.get_federation_url(),
        'name': tf.track.full_name,
        'published': tf.creation_date.isoformat(),
        'updated': tf.modification_date.isoformat(),
        'metadata': {
            'artist': {
                'name': tf.track.artist.name,
                'musicbrainz_id': None,
            },
            'release': {
                'title': tf.track.album.title,
                'musicbrainz_id': None,
            },
            'recording': {
                'title': tf.track.title,
                'musicbrainz_id': None,
            },
        },
        'url': {
            'href': utils.full_url(tf.path),
            'type': 'Link',
            'mediaType': 'audio/mp3'
        },
        'attributedTo': [
            library.url
        ]
    }

    serializer = serializers.AudioSerializer(tf, context={'actor': library})

    assert serializer.data == expected


def test_collection_serializer_to_ap(factories):
    tf1 = factories['music.TrackFile'](mimetype='audio/mp3')
    tf2 = factories['music.TrackFile'](mimetype='audio/ogg')
    library = actors.SYSTEM_ACTORS['library'].get_actor_instance()
    expected = {
        '@context': serializers.AP_CONTEXT,
        'id': 'https://test.id',
        'actor': library.url,
        'totalItems': 2,
        'type': 'Collection',
        'items': [
            serializers.AudioSerializer(
                tf1, context={'actor': library, 'include_ap_context': False}
            ).data,
            serializers.AudioSerializer(
                tf2, context={'actor': library, 'include_ap_context': False}
            ).data,
        ]
    }

    collection = {
        'id': expected['id'],
        'actor': library,
        'items': [tf1, tf2],
        'item_serializer': serializers.AudioSerializer
    }
    serializer = serializers.CollectionSerializer(
        collection, context={'actor': library, 'id': 'https://test.id'})

    assert serializer.data == expected