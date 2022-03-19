# Generated by Django 3.2.10 on 2022-02-15 16:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_groupname_groupname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupname',
            name='groupname',
            field=models.UUIDField(default=uuid.uuid1, editable=False, unique=True),
        ),
    ]
