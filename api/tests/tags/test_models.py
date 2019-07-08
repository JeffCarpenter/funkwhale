import pytest

from funkwhale_api.tags import models


@pytest.mark.parametrize(
    "existing, given, expected",
    [
        ([], ["tag1"], ["tag1"]),
        (["tag1"], ["tag1"], ["tag1"]),
        (["tag1"], ["tag2"], ["tag1", "tag2"]),
        (["tag1"], ["tag2", "tag3"], ["tag1", "tag2", "tag3"]),
    ],
)
def test_add_tags(factories, existing, given, expected):
    obj = factories["music.Artist"]()
    for tag in existing:
        factories["tags.TaggedItem"](content_object=obj, tag__name=tag)

    models.add_tags(obj, *given)

    tagged_items = models.TaggedItem.objects.all()

    assert tagged_items.count() == len(expected)
    for tag in expected:
        match = tagged_items.get(tag__name=tag)
        assert match.content_object == obj


@pytest.mark.parametrize(
    "existing, given, expected",
    [
        ([], ["tag1"], ["tag1"]),
        (["tag1"], ["tag1"], ["tag1"]),
        (["tag1"], [], []),
        (["tag1"], ["tag2"], ["tag2"]),
        (["tag1", "tag2"], ["tag2"], ["tag2"]),
        (["tag1", "tag2"], ["tag3", "tag4"], ["tag3", "tag4"]),
    ],
)
def test_set_tags(factories, existing, given, expected):
    obj = factories["music.Artist"]()
    for tag in existing:
        factories["tags.TaggedItem"](content_object=obj, tag__name=tag)

    models.set_tags(obj, *given)

    tagged_items = models.TaggedItem.objects.all()

    assert tagged_items.count() == len(expected)
    for tag in expected:
        match = tagged_items.get(tag__name=tag)
        assert match.content_object == obj
