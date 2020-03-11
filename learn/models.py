from django.db.models import *
from django.urls import reverse
from django_summernote import fields

# Create your models here.
from learn.lib.utils import formatPath


class Subject(Model):
    name = CharField(max_length=200, help_text='Enter the name of a subject.')

    def get_absolute_url(self):
        return reverse('unit_list', args=[str(self)])

    def __str__(self):
        return self.name.replace(" ", "_")

class Course(Model):
    name = CharField(max_length=200, help_text='Enter the name of a course.')
    subject = ForeignKey(Subject, on_delete=SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('course', args=[str(self.subject), str(self)])

    def __str__(self):
        return formatPath(self.name)

class Article(Model):
    title = CharField(max_length=60, help_text='Enter the title for this article.', primary_key=True,
                      default='Title')
    body = TextField(help_text='Enter the body for this article.', default='Body')
    topic = ManyToManyField(Course, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('article', args=[str(self)])

    def __str__(self):
        return self.title.replace(" ", "_")

class Practice(Model):
    article = ForeignKey(Article, on_delete=SET_NULL, blank=True, null=True)
    number = IntegerField(help_text='Enter the order number of this practice node.', null=True)

    class Meta:
        ordering = ['number']

    def get_absolute_url(self):
        return reverse('practice',
                       args=[str(self.article), str(self.number)])

    def __str__(self):
        return f'{self.article.title} {self.number}'

class Question(Model):
    prompt = TextField(max_length=1000, help_text='Enter the prompt for this question.')
    TYPES = (
        ('W', 'Writing'),
        ('S', 'Selection'),
    )
    type = CharField(max_length=1, choices=TYPES, default='W', help_text='Type of question.')
    practice = ForeignKey(Practice, on_delete=SET_NULL, blank=True, null=True)

    # def get_absolute_url(self):
    # return reverse('question', args=[str(self.topic.unit.language), str(self.topic.unit), str(self.topic), str(self.number)])


class Answer(Model):
    long = TextField(max_length=1000, help_text='Enter a long answer for this question (can be several sentences).',
                     blank=True, null=True)
    short = CharField(max_length=200, help_text='Enter a short answer for this question (can be several words).',
                      blank=True, null=True)
    # image = ImageField(help_text='Upload an image for this answer', blank=True, null=True)
    question = ForeignKey(Question, on_delete=SET_NULL, blank=True, null=True)
