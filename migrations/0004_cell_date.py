# Generated by Django 2.2.6 on 2020-08-07 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0003_cell_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
