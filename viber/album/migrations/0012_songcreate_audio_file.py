# Generated by Django 2.0.7 on 2018-07-26 20:33

import album.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0011_auto_20180727_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='songcreate',
            name='audio_file',
            field=models.FileField(default='', upload_to=album.models.upload_image_path),
        ),
    ]
