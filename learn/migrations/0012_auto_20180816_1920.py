# Generated by Django 2.1 on 2018-08-16 23:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0011_auto_20180816_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='ID for this question.', primary_key=True, serialize=False),
        ),
    ]