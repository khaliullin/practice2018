# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-15 11:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=50, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_users', to='cards.Card')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEdges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=50, null=True)),
                ('card_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_from_closures', to='cards.Card')),
                ('card_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_to_closures', to='cards.Card')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_edges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='closure',
            name='card_from',
        ),
        migrations.RemoveField(
            model_name='closure',
            name='card_to',
        ),
        migrations.DeleteModel(
            name='Closure',
        ),
        migrations.AlterUniqueTogether(
            name='useredges',
            unique_together=set([('user', 'card_from', 'card_to'), ('session_key', 'card_from', 'card_to')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercards',
            unique_together=set([('user', 'card'), ('session_key', 'card')]),
        ),
    ]