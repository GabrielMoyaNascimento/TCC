# Generated by Django 2.2.10 on 2020-04-14 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0013_auto_20200414_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupom',
            name='validade',
            field=models.DateTimeField(null=True, verbose_name='data de validade'),
        ),
    ]