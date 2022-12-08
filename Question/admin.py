from django.contrib import admin
from Question.models import Topic, Test, Question, Answer
from django.template.loader import get_template
import nested_admin
from django.core.exceptions import ValidationError
from django.contrib import messages

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    fields = ('title',)
    

# class TopicInLine(admin.StackedInline):
#     model = Test.topics.through
#     extra = 1
    
    
# class QuestionInLineFormset(BaseInlineFormSet): 
#     def clean(self):
#         count = 0
#         for form in self.forms:
#             try:
#                 if form.cleaned_data:
#                     count += 1
#             except AttributeError:
#                 pass
#         if count < 1:
#             raise form.ValidationError('Должен быть хотя бы 1 правильный вариант')
 

# class AnswerInLine(admin.StackedInline):
#     model = Answer
 
        
# class QuestionInLine(admin.StackedInline):
#     extra = 1
#     formset = QuestionInLineFormset
#     model = Question
#     inlines = [AnswerInLine,]
    
    

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ('test', 'text', 'image', 'type', 'exact_answer_flag', 'score')
#     inlines = [AnswerInLine,]
    
    
# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     fields = ('question', 'text', 'image')
    
    
# @admin.register(CorrectAnswer)
# class CorrectAnswerAdmin(admin.ModelAdmin):
#     fields = ('question', 'answer') 
    
    

# @admin.register(Test)
# class TestAdmin(admin.ModelAdmin):
#     fields = ('name',)
#     inlines = [TopicInLine, QuestionInLine]
    
    
# class QuestionInLineNew(admin.StackedInline):
#     model = Question
#     fields = ('text', 'image', 'type', 'exact_answer_flag', 'score')
#     extra = 1
    
#     def answer_inline(self, obj=None, *args, **kwargs):
#         context = getattr(self.modeladmin.response, 'context_data', None) or {}
#         admin_view = ProductModelAdmin(self.model, self.modeladmin.admin_site).add_view(self.modeladmin.request)
#         inline = admin_view.context_data['inline_admin_formsets'][0]
#         return get_template(inline.opts.template).render(context | {'inline_admin_formset': inline}, self.modeladmin.request)



# class TopicInline(nested_admin.NestedStackedInline):
#     #model = Test.topics.through
#     model = Topic
#     extra = 1
    

class AnswerInLineFormset(nested_admin.NestedInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    if form.cleaned_data['correct_flag']:
                        count += 1
            except AttributeError:
                pass
        if count == 0 or count == len(self.forms):
            if count == 1:
                raise ValidationError("Должен быть хотя бы 1 правильный вариант")
            else:
                raise ValidationError("Все варианты не могут быть правильными")


class AnswerInLine(nested_admin.NestedStackedInline):
    model = Answer
    extra = 0
    formset = AnswerInLineFormset


class QuestionInLine(nested_admin.NestedStackedInline):
    model = Question
    inlines  = [AnswerInLine]
    extra = 0
    fields = ('text', 'type', 'score')



class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInLine]
    fields = ('name', 'topic')
    
    def save_model(self, request, obj, form, change):
        if change:
            messages.add_message(request, messages.WARNING, 'Был изменён вопрос! Проверьте правильность ответов!')
        super(TestAdmin, self).save_model(request, obj, form, change)
    
admin.site.register(Test, TestAdmin)


from django.contrib.auth.models import Group
admin.site.unregister(Group)