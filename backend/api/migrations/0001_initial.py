# Generated by Django 5.0.3 on 2024-04-08 00:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='Camera', max_length=50)),
                ('status', models.CharField(choices=[('ON', 'On'), ('OFF', 'Off'), ('DIS', 'Disconnected')], default='OFF', max_length=3)),
                ('ip', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('people_in', models.PositiveBigIntegerField()),
                ('people_out', models.PositiveBigIntegerField()),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.camera')),
            ],
            options={
                'ordering': ['-time', 'camera'],
                'indexes': [models.Index(fields=['camera', '-time'], name='api_metadat_camera__d6b80b_idx')],
            },
        ),
    ]