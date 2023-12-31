# Generated by Django 4.2.7 on 2023-12-02 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fitness_goal', models.CharField(choices=[('Get Stronger', 'Get Stronger'), ('Gain Muscle', 'Gain Muscle'), ('Lose Fat', 'Lose Fat')], max_length=255)),
                ('frequency', models.IntegerField(choices=[(1, '1 day per week'), (2, '2 days per week'), (3, '3 days per week'), (4, '4 days per week'), (5, '5 days per week'), (6, '6 days per week'), (7, '7 days per week')], default=1)),
                ('workout_duration', models.IntegerField(default=0)),
                ('overall_intensity', models.CharField(choices=[('High Intensity', 'High Intensity'), ('Medium Intensity', 'Medium Intensity'), ('Low Intensity', 'Low Intensity')], max_length=255)),
                ('focused_muscle_groups', models.JSONField(default=list)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
