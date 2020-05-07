# Generated by Django 3.0.4 on 2020-05-05 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0051_auto_20200319_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='checksum',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='uploadversion',
            name='mimetype',
            field=models.CharField(choices=[('audio/mp3', 'mp3'), ('audio/mpeg3', 'mp3'), ('audio/x-mp3', 'mp3'), ('audio/mpeg', 'mp3'), ('video/ogg', 'ogg'), ('audio/ogg', 'ogg'), ('audio/opus', 'opus'), ('audio/x-m4a', 'aac'), ('audio/x-m4a', 'm4a'), ('audio/x-flac', 'flac'), ('audio/flac', 'flac')], max_length=50),
        ),
    ]
