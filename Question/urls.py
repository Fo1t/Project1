from django.urls import path
from Question.views import Main, TestPage, TestResultPage

urlpatterns = [
    path('', Main, name='main'),
    path('<int:test_id>', TestPage, name='test'),
    path('result/<int:test_id>', TestResultPage, name='result')
]