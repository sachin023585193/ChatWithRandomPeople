# Generated by Django 3.2.12 on 2022-02-17 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20220216_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='privateChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='privateRoomUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=200, null=True)),
                ('ownergroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='privateRoomUsers', to='chat.privatechat')),
            ],
        ),
    ]
