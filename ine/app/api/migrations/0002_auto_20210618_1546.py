# Generated by Django 3.0 on 2021-06-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Director',
                'verbose_name_plural': 'Director',
            },
        ),
        migrations.AlterField(
            model_name='database',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Name'),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200, unique=True, verbose_name='Name')),
                ('release_date', models.DateTimeField(verbose_name='release date')),
                ('imdb_ranking', models.FloatField()),
                ('database', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='database', to='api.Database', verbose_name='Database')),
                ('director', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='director', to='api.Director', verbose_name='Director')),
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movies',
            },
        ),
    ]
