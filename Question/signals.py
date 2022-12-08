from django.dispatch import receiver
from django.db.models.signals import pre_delete
from Question.models import Question, Answer


@receiver(pre_delete, sender=Question)
def question_handler(sender, **kwargs):
    print(f'____________________________________________________')
    print(f'Signal question_handler')
    print(f'{sender}= ')
    print(f'{kwargs}= ')
    print(f'____________________________________________________')
    Answer.objects.filter(question=sender).delete()