# Generated by Django 2.1 on 2018-08-12 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_question_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name for this topic.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UnitNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name for this unit.', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='topicnode',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.UnitNode'),
        ),
        migrations.AddField(
            model_name='practicenode',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.TopicNode'),
        ),
    ]