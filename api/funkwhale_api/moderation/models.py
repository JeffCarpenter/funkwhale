import urllib.parse
import uuid

from django.db import models
from django.utils import timezone


class InstancePolicyQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def matching_url(self, url):
        parsed = urllib.parse.urlparse(url)
        return self.filter(
            models.Q(target_domain_id=parsed.hostname) | models.Q(target_actor__fid=url)
        )


class InstancePolicy(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    actor = models.ForeignKey(
        "federation.Actor",
        related_name="created_instance_policies",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    target_domain = models.OneToOneField(
        "federation.Domain",
        related_name="instance_policy",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    target_actor = models.OneToOneField(
        "federation.Actor",
        related_name="instance_policy",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    creation_date = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    # a summary explaining why the policy is in place
    summary = models.TextField(max_length=10000, null=True, blank=True)
    # either block everything (simpler, but less granularity)
    block_all = models.BooleanField(default=False)
    # or pick individual restrictions below
    # do not show in timelines/notifications, except for actual followers
    silence_activity = models.BooleanField(default=False)
    silence_notifications = models.BooleanField(default=False)
    # do not download any media from the target
    reject_media = models.BooleanField(default=False)

    objects = InstancePolicyQuerySet.as_manager()

    @property
    def target(self):
        if self.target_actor:
            return {"type": "actor", "obj": self.target_actor}
        if self.target_domain_id:
            return {"type": "domain", "obj": self.target_domain}
