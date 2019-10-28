# Generated by Django 2.2.5 on 2019-10-21 17:05

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import funkwhale_api.music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0040_auto_20191021_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='upload',
            name='from_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='federation.Activity'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='import_details',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=funkwhale_api.music.models.empty_dict, encoder=django.core.serializers.json.DjangoJSONEncoder, max_length=50000),
        ),
        migrations.AlterField(
            model_name='upload',
            name='import_metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=funkwhale_api.music.models.empty_dict, encoder=django.core.serializers.json.DjangoJSONEncoder, max_length=50000),
        ),
        migrations.AlterField(
            model_name='upload',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=funkwhale_api.music.models.empty_dict, encoder=django.core.serializers.json.DjangoJSONEncoder, max_length=50000),
        ),
        migrations.AlterField(
            model_name='uploadversion',
            name='mimetype',
            field=models.CharField(choices=[('video/ogg', 'ogg'), ('audio/ogg', 'ogg'), ('audio/opus', 'opus'), ('audio/mpeg', 'mp3'), ('audio/x-m4a', 'aac'), ('audio/x-m4a', 'm4a'), ('audio/x-flac', 'flac'), ('audio/flac', 'flac')], max_length=50),
        ),
    ]