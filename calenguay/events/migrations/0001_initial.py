# Generated by Django 3.0.4 on 2020-03-23 21:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(60)])),
                ('max_booking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Tiempo máximo de reserva (en dias)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available', max_length=12)),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
                ('ruletype', models.CharField(choices=[('dow', 'Day of the week'), ('date', 'Until date')], max_length=4)),
                ('rule_dow', models.IntegerField(blank=True, choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], null=True)),
                ('rule_from_date', models.DateField(blank=True, null=True)),
                ('rule_to_date', models.DateField(blank=True, null=True)),
                ('eventtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='events.EventType')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField()),
                ('ends_at', models.DateTimeField()),
                ('eventtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.EventType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='users',
            field=models.ManyToManyField(blank=True, through='events.UserCategory', to=settings.AUTH_USER_MODEL),
        ),
    ]
