# Generated by Django 2.1 on 2018-08-16 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_practicenode_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='practicenode',
            options={'ordering': ['number']},
        ),
        migrations.RemoveField(
            model_name='practicenode',
            name='name',
        ),
    ]
