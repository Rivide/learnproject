from django.contrib import admin

# Register your models here.
from .models import Practice, Question, Answer, Subject, Course, Article


class CoursesInline(admin.TabularInline):
    model = Course


class ArticlesInline(admin.TabularInline):
    model = Article


class PracticesInline(admin.TabularInline):
    model = Practice


class QuestionsInline(admin.TabularInline):
    model = Question


class AnswersInline(admin.TabularInline):
    model = Answer
    extras = 4
    max_num = 4
    min_num = 4


@admin.register(Subject)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CoursesInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ArticlesInline]

@admin.register(Practice)
class PracticeNodeAdmin(admin.ModelAdmin):
    list_display = ('topic', 'number',)
    inlines = [QuestionsInline]

    def get_ordering(self, request):
        return ['topic', 'number']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('practice', 'prompt', 'type')
    inlines = [AnswersInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('long', 'short')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)