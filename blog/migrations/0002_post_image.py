# Generated by Django 3.0.4 on 2020-04-06 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.FileField(default=0, upload_to='pics'),
            preserve_default=False,
        ),
    ]
