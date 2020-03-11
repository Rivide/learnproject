from django.shortcuts import render
from django.forms import inlineformset_factory, ModelForm
from django_summernote.widgets import SummernoteInplaceWidget

from .models import Question, Answer, Subject, Course, Practice, Article
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404


from .forms import QuizForm, ArticleCreateForm
from .lib.utils import formatPath, pathToString

# Create your views here.
def index(request):
    return render(request, 'index.html')


def tree(request):
    return render(request, 'index.html', {'units'})


def practice(request, **kwargs):
    return HttpResponseRedirect(
        reverse('question', args=[kwargs['lang'], kwargs['unit'], kwargs['topic'], kwargs['practice'], 1]))


def question(request, **kwargs):
    return render


def topic(request):
    return

class QuestionCreate(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'learn/article.html'

    def get_object(self):
        print('article detail view get object')
        print(self.kwargs)
        print(self.request.GET)
        return get_object_or_404(Article, pk=self.kwargs['title'].replace('_', ' '))

class ArticleCreateView(generic.CreateView):
    model = Article
    fields = '__all__'
    template_name = 'learn/article_create.html'
    widgets = {
        'body': SummernoteInplaceWidget()
    }
    def get_form(self):
        form = super().get_form()
        form.fields['body'].widget = SummernoteInplaceWidget()
        return form

    def get_success_url(self):
        print('article create')
        print(str(self.object))
        return reverse('article', args=[str(self.object)])

class ArticleUpdateView(generic.UpdateView):
    model = Article
    template_name = 'learn/article_update.html'
    fields = '__all__'

    def get_form(self):
        form = super().get_form()
        form.fields['body'].widget = SummernoteInplaceWidget()
        return form

    def get_object(self):
        return get_object_or_404(Article, pk=pathToString(self.kwargs['title']))
    def get_success_url(self):
        return reverse('article', args=[str(self.object)])

class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'learn/quiz.html'

    def get_object(self):
        return get_object_or_404(Question, pk=self.get_queryset()[0].id)

    def get_queryset(self):
        practicenode = Practice.objects.filter(article__title=modelStrToName(self.kwargs['title']),
                                               number=self.kwargs['practice'])
        print(f'{practicenode} {Question.objects.count()} hiii')
        id = practicenode[0].question_set.all()[int(self.kwargs['question']) - 1].id
        return Question.objects.filter(  # practice__topic__name=self.kwargs['topic'],
            # practice__number=self.kwargs['practice'],
            id=id)


def question_view(request, **kwargs):
    practicenode = Practice.objects.filter(article__title=modelStrToName(kwargs['title']),
                                               number=kwargs['practice'])
    # print(f'{practicenode} {Question.objects.count()} hiii')
    questions = request.session.get('questions', [q.id for q in practicenode[0].question_set.all().order_by('?')])
    request.session['questions'] = questions
    score = request.session.get('score', [])
    request.session['score'] = score
    qno = request.session.get('qno', 0)
    if qno >= len(questions):
        context = {'questions': questions, 'score': score}
        del request.session['questions']
        del request.session['qno']
        del request.session['score']
        return render(request, 'learn/results.html', context)

    print(qno)
    question_inst = get_object_or_404(Question, pk=questions[qno])
    context = {'question': question_inst}
    print(f'{questions} {qno} {id} ')
    if request.method == 'POST':
        currentform = QuizForm(request.POST, initial={
            'prompt': question_inst.prompt})  # """, initial={'prompt': question_inst.prompt}"""
        print(f' {currentform["answer"].field.widget.attrs} {currentform["questionclosed"].value()}')
        if not currentform["questionclosed"].value():
            context['answers'] = [answer.long for answer in question_inst.answer_set.all()]
            if currentform.is_valid():
                context['incorrect'] = False
                if len(score) > qno:
                    score[qno] += 1
                else:
                    score.append(1)
                qno += 1
                form = QuizForm(initial={'prompt': question_inst.prompt, 'answer': request.POST.get('answer', ''),
                                         'questionclosed': True})
                form['answer'].field.widget.attrs['readonly'] = 'readonly'
                print(f'HOO {form["questionclosed"].value()}')
            else:
                if len(score) <= qno:
                    context['incorrect'] = True
                    context.pop('answers', None)
                    score.append(-1)
                    form = QuizForm(initial={'prompt': question_inst.prompt, 'questionclosed': False})
                else:
                    qno += 1
                    context['incorrect'] = True
                    form = QuizForm(initial={'prompt': question_inst.prompt, 'answer': request.POST.get('answer', ''),
                                             'questionclosed': True})
                    form['answer'].field.widget.attrs['readonly'] = 'readonly'
        else:
            form = QuizForm(initial={'prompt': question_inst.prompt, 'questionclosed': False})
    else:
        form = QuizForm(initial={'prompt': question_inst.prompt, 'questionclosed': False})
    request.session['qno'] = qno
    request.session['score'] = score
    context['score'] = score
    context['form'] = form
    return render(request, 'learn/quiz2.html', context)


question_view.questions = None
question_view.qnum = 0


def modelStrToName(str):
    return str.replace("-", " ").title()


def question_create(request):
    question_form = QuestionCreate()
    question = Question()
    QuestionInlineFormSet = inlineformset_factory(Question, Answer, fields='__all__')
    formset = QuestionInlineFormSet(instance=question)
    if request.method == 'POST':
        formset = QuestionInlineFormSet(request.POST)
        question = QuestionCreate(request.POST)
        created_question = question.save()
        formset = QuestionInlineFormSet(request.POST, instance=created_question)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('question_create'))
    else:
        formset = QuestionInlineFormSet()
    return render(request, 'learn/create.html', {'formset': formset, 'qformset': question_form})


def article_create(request, **kwargs):
    if request.method == 'POST':
        print('article_create POST')
        new_article = ArticleCreateForm(request.POST).save()
        return HttpResponseRedirect(reverse('article', args=[str(new_article)]))

    print('article_create GET')
    return render(request, 'learn/article_create.html', {'form': ArticleCreateForm()})


class ArticleListView(generic.ListView):
    model = Article

    def get_queryset(self):
        return super().get_queryset().filter(course__name=self.kwargs['course'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['course'] = self.kwargs['course']
        return data


class SubjectListView(generic.ListView):
    model = Subject
