# Generated by Django 4.2.5 on 2023-09-28 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'User profile',
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Seller', 'Seller'), ('Admin', 'Admin')], default='Admin', max_length=32, verbose_name='User type'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='user.userprofile', verbose_name='User type'),
        ),
    ]
