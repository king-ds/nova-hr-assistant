# Generated by Django 2.0.13 on 2019-09-03 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='reaction_given',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='reaction_received',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='reaction_type',
            field=models.CharField(max_length=100),
        ),
    ]
