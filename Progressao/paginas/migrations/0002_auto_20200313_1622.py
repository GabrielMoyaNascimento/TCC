# Generated by Django 2.2.10 on 2020-03-13 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='cidade',
        ),
        migrations.DeleteModel(
            name='Cidade',
        ),
        migrations.DeleteModel(
            name='Estado',
        ),
        migrations.DeleteModel(
            name='Pessoa',
        ),
    ]
