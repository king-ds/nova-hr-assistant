# Generated by Django 2.0.13 on 2019-09-02 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('num_of_employees', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('datetime_joined', models.DateTimeField(auto_now_add=True)),
                ('total_votes', models.IntegerField(default=0)),
                ('prediction', models.BooleanField(default=True)),
                ('selected_vote', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gmail_authentication.Department')),
            ],
        ),
    ]
