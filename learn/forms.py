from django.forms import *
from django_summernote.widgets import SummernoteInplaceWidget

from .models import Question, Answer, Article
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404



#AnswerFormSet = inlineformset_factory(Question, Answer, fields=('prompt', 'long', 'short'))

class ArticleCreateForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'title': SummernoteInplaceWidget(),
            'body': SummernoteInplaceWidget()
        }

class QuizForm(Form):
    prompt = CharField(max_length=1000, widget=Textarea(attrs={"readonly":"readonly"}), label='', required=False)
    answer = CharField(max_length=1000, widget=Textarea, label='')
    questionclosed = BooleanField(label='', required=False)

    def clean(self):
        data = super().clean()
        question = get_object_or_404(Question, prompt=data.get('prompt'))
        answer = data.get('answer')
        if not answer in [a.long for a in question.answer_set.all()]:
            print(f'{answer} {question.answer_set.all()[0].long} {data}')
            raise ValidationError(_('Incorrect'))
        else:
            print(f'{answer} {question.answer_set.all()[0].long} {data}')


    """def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)"""