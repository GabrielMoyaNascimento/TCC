# Generated by Django 2.2.10 on 2020-04-06 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0011_auto_20200406_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='desconto',
            field=models.CharField(blank=True, choices=[('00%', 'Venda sem desconto'), ('05%', '05%'), ('10%', '10%'), ('15%', '15%'), ('20%', '20%'), ('25%', '25%'), ('35%', '35%'), ('40%', '40%'), ('45%', '45%'), ('50%', '50%'), ('60%', '60%'), ('70%', '70%'), ('75%', '75%')], max_length=4, null=True),
        ),
    ]
