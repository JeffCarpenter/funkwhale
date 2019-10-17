# Generated by Django 2.2.4 on 2019-09-20 08:57

import datetime
from django.conf import settings

from django.db import migrations, models
import django.utils.timezone
import funkwhale_api.users.models


def set_display_date(apps, schema_editor):
    """
    Set display date for instance/funkwhale support message on existing users
    """
    User = apps.get_model("users", "User")
    now = django.utils.timezone.now()
    instance_support_message_display_date = now + datetime.timedelta(days=settings.INSTANCE_SUPPORT_MESSAGE_DELAY)
    funkwhale_support_message_display_date = now + datetime.timedelta(days=settings.FUNKWHALE_SUPPORT_MESSAGE_DELAY)

    User.objects.update(instance_support_message_display_date=instance_support_message_display_date)
    User.objects.update(funkwhale_support_message_display_date=funkwhale_support_message_display_date)


def rewind(*args, **kwargs):
    pass



class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_application_scope'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='funkwhale_support_message_display_date',
            field=models.DateTimeField(blank=True, null=True, default=funkwhale_api.users.models.get_default_funkwhale_support_message_display_date),
        ),
        migrations.AddField(
            model_name='user',
            name='instance_support_message_display_date',
            field=models.DateTimeField(blank=True, null=True, default=funkwhale_api.users.models.get_default_instance_support_message_display_date),
        ),
        migrations.RunPython(set_display_date, rewind),
    ]