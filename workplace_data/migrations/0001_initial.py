# Generated by Django 2.0.13 on 2019-09-18 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workplace_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=255)),
                ('updated_time', models.DateTimeField()),
                ('message', models.TextField()),
            ],
        ),
    ]
