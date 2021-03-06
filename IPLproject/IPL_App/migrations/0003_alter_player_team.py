# Generated by Django 3.2 on 2021-11-21 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IPL_App', '0002_alter_player_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(blank=True, db_column='team', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player', to='IPL_App.team', to_field='teamName'),
        ),
    ]
