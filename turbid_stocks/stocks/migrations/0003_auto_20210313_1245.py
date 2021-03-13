# Generated by Django 3.1.7 on 2021-03-13 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_auto_20210313_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='isin',
            field=models.CharField(default='none', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='symbol',
            name='lot',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='figi',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='ticker',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
