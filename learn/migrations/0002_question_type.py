# Generated by Django 2.1 on 2018-08-12 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('W', 'Writing'), ('S', 'Selection')], default='W', help_text='Type of question.', max_length=1),
        ),
    ]
