# Generated by Django 5.0 on 2024-01-07 13:11

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='Language Code')),
                ('name', models.CharField(max_length=100, verbose_name='Language Name')),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Project Name')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Project Description')),
                ('client', models.CharField(max_length=100, verbose_name='Client')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='Site Code')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Site Name')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Country')),
                ('postal_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Postal Code')),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1, verbose_name='Floor Number')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Floor Name')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floors', to='staff_module.site', verbose_name='Site')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('contract', models.CharField(choices=[('civil', 'Civil'), ('labour', 'Labour'), ('b2b', 'B2B')], default='civil', max_length=10, verbose_name='Contract Type')),
                ('is_manager', models.BooleanField(default=False, verbose_name='Is Manager')),
                ('is_team_lead', models.BooleanField(default=False, verbose_name='Is Team Lead')),
                ('is_administrator', models.BooleanField(default=False, verbose_name='Is Administrator')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('office_floors', models.ManyToManyField(blank=True, to='staff_module.floor', verbose_name='Office Floors')),
                ('language', models.ForeignKey(default='eng', null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff_module.language', verbose_name='Language')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff_module.site', verbose_name='Site')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Team Name')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Team Description')),
                ('languages', models.ManyToManyField(blank=True, null=True, to='staff_module.language', verbose_name='Languages')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff_module.projects', verbose_name='Project')),
                ('team_lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Team Lead')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='staff_module.teams', verbose_name='Team'),
        ),
    ]
