# Generated by Django 3.2 on 2021-04-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_file_server_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='host',
            field=models.CharField(default='Host1', max_length=100),
            preserve_default=False,
        ),
    ]
