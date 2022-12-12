from django.shortcuts import render, redirect
from Question.models import Test, Question, Answer
from Question.forms import QuestionForm
from Profile.models import UserTest, UserAnswer
from django import forms
from django.conf import settings


def Main(request):
    '''
    Отрисовка главной страницы
    '''
    data = {} # Инициализация контекста
    tests = [] # Инициализация списка тестов
    if not request.user.is_authenticated:
        return redirect('auth/login')
    status_list = ['в', 'о', 'п', 'з'] # Список возможных статусов
    for status in status_list:
        for ut in UserTest.objects.filter(user=request.user, status=status):
            tests.append({
                'id': ut.test.id,
                'test_name': ut.test.name,
                'test_topic': ut.test.topic.title,
                'score': ut.score,
                'ut': ut,
                })
    data['tests'] = tests
    return render(request, 'index.html', data)


def GetQuestion(user, test_id):
    '''
        Попытка получения вопроса.
        user - Пользователь.
        test_id - id Теста.
        Возвращает Null Если вопросы закончились и/или были не найдены.
    '''
    if Test.objects.filter(id=test_id).exists(): # Проверка наличия теста.
        if Question.objects.filter(test=test_id).exists(): # Проверка наличия вопросов у теста.
            test = Test.objects.get(id=test_id)
            lst_q = Question.objects.filter(test=test).order_by('-index')[0]
            last_question = UserTest.objects.get(user=user, test=test)
            temp = Question.objects.filter(test=test, index__lte=last_question.last_question).order_by('-index')[0]
            if UserTest.objects.get(user=user, test=test).last_question != Question.objects.filter(test=test).order_by('-index')[0].index + 1: # Проверка наличия доступных вопросов.
                return Question.objects.filter(test=test, index__lte=last_question.last_question).order_by('-index')[0]
            else: # Если вопросов не осталось
                ut = UserTest.objects.get(user=user, test=Test.objects.get(id=test_id))
                ut.status = 'п'
                ut.save()
                next_test = Test.objects.filter(topic=ut.test.topic, index__gt=ut.test.index).order_by('index')
                if next_test.exists():
                    next_test = next_test[0] if type(next_test) is list else next_test
                    next_usertest = UserTest.objects.get(user=user, test=list(next_test)[0])
                    next_usertest.status = 'о'
                    next_usertest.save()
    return None
    
    
def FormsGenerate(question):
    '''
        Генерация полей формы.
        question: Question - Вопрос по которому бедут сгенерированна форма 
        Возвращает QuestionForm.
    '''
    new_form = QuestionForm()
    new_form.fields[f'{question.id}_text'] = forms.CharField(initial=question.text,
                                                             required=False,
                                                             widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                                             label='',
                                                             )
    ANSWER_CHOICES = []
    for answer in  Answer.objects.filter(question=question):
        ANSWER_CHOICES.append((str(answer.id), answer.text))
    new_form.fields['answers'] = forms.ChoiceField(choices = ANSWER_CHOICES, widget=forms.CheckboxSelectMultiple())
    return new_form





def access_check(request, test_id, question_id=None):
    '''
    Проверка доступа и доступности теста/вопроса
    '''
    if not Test.objects.filter(id=test_id).exists():
        return False
    if not Question.objects.filter(id=question_id).exists():
        return False
    test = Test.objects.get(id=test_id)
    ut = UserTest.objects.get(user=request.user, test=test)
    if ut.status == 'з':
        return False
    qs = Question.objects.get(id=question_id)
    return True
    
 
def CheckAnswers(request):
    '''
        Обработка ответа пользователя
    '''
    question_id = list(request.POST)[0].split('_')[0]
    question = Question.objects.get(id=question_id)
    score = 0
    if (len(request.POST.getlist('answers')) != 0 and
        len(request.POST.getlist('answers')) != len(Answer.objects.filter(question=question)) and
        question.score != 0.0):
        for answer in request.POST.getlist('answers'):
            if Answer.objects.filter(id=answer).exists():
                UserAnswer(user=request.user, question=question, answer=Answer.objects.get(id=answer)).save()
                print(f'{Answer.objects.get(id=answer).correct_flag=}')
                if Answer.objects.get(id=answer).correct_flag == True:
                    coefficient = question.score / len(Answer.objects.filter(question=question, correct_flag=True))
                    score += question.score / coefficient
    user_test = UserTest.objects.get(user=request.user, test=question.test)
    user_test.score = score
    user_test.last_question = question.index + 1
    user_test.save()
    
    

def TestPage(request, test_id):
    '''
        Отрисовка страницы теста
    '''
    if not request.user.is_authenticated:
        return redirect('')
    question = GetQuestion(request.user, test_id)
    if question is not None:
        if access_check(request, test_id, question.id):
            data = {}
            if request.method == 'GET':
                form = FormsGenerate(question=question)
                data = {'form': form}
                return render(request, 'test.html', data)
            else:
                CheckAnswers(request)
                question = GetQuestion(request.user, test_id)
                if question is not None:
                    form = FormsGenerate(question=question)
                else:
                    return redirect('./')
                return redirect(f'/{test_id}')
        else:
            return redirect('./')
    else:
        return redirect('./')
    
    
def TestResultPage(request, test_id):
    '''
        Отрисовка страницы с результатами теста
    '''
    data = {}
    if Test.objects.filter(id=test_id).exists():
        test = Test.objects.get(id=test_id)
        data['test'] = test
        if UserTest.objects.filter(user=request.user, test=test):
            user_test = UserTest.objects.get(user=request.user, test=test)
            data['ut'] = user_test 
            questions = Question.objects.filter(test=test)
            qa = []
            user_score = user_test.score
            all_score = 0
            for question in Question.objects.filter(test=test):
                all_score += question.score
            for qustion in questions:
                qa.append(
                    {
                        'qustion': qustion,
                        'answers': Answer.objects.filter(question=qustion),
                        'user_answers': UserAnswer.objects.filter(user=request.user, question=qustion),
                        'correct_answers': Answer.objects.filter(question=qustion, correct_flag=True),
                    }
                )
            data['percent'] = int((user_score / all_score) * 100)
            data['qa'] = qa
    print(f'{data["qa"]=}')
    return render(request, 'test_result.html', data)