from django.db import models
from django.contrib.auth.models import User
from Question.models import Test, Topic, Question, Answer

    
class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('о', 'Открыт'),
        ('п', 'Пройден'),
        ('з', 'Закрыт'),
        ('в', 'В процессе'),
    ]
    status = models.CharField(max_length=1, default='',choices=STATUS_CHOICES)
    last_question = models.PositiveIntegerField(blank=False, default=0)
    score = models.PositiveIntegerField(blank=False, default=0)
    
class UserTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    last_completed_test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserQuestion_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='UserQuestion_question')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='UserQuestion_answers')


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User, dispatch_uid="update_user_test_topic")
def update_user_test_topic(sender, instance, **kwargs):
    if not UserTopic.objects.filter(user=instance).exists():
        for topic in Topic.objects.all():
            UserTopic(
                user=instance,
                topic=topic
            ).save()
    if not UserTest.objects.filter(user=instance).exists():
        for test in Test.objects.all():
            UserTest(
                user=instance,
                test=test,
                status='о' if test.index==0 else 'з',
                last_question=0,
                score=0
            ).save()
            
        
@receiver(post_save, sender=Topic, dispatch_uid="update_user_topic")
def update_user_topic(sender, instance, **kwargs):
    print('update_user_topic')
    if not UserTopic.objects.filter(topic=instance).exists():
        for user in User.objects.all():
            UserTopic(
                user=user,
                topic=instance
            ).save()