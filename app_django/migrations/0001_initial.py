# Generated by Django 4.2 on 2023-04-15 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_menu', models.CharField(max_length=30, verbose_name='Название меню')),
                ('position', models.IntegerField(verbose_name='Позиция вложенности')),
                ('url', models.TextField(db_index=True, unique=True, verbose_name='URL')),
                ('top_menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_django.menumodel', verbose_name='Пункт предыдущего меню')),
            ],
            options={
                'verbose_name': 'Меню сайта',
                'verbose_name_plural': 'Меню сайта',
                'ordering': ['id'],
            },
        ),
    ]