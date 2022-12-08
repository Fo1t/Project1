from django.db import models
from uuid import uuid1


class Topic(models.Model):
    title = models.CharField(unique=True, blank=False, max_length=50)
    
    def __str__(self):
        return f'{self.title}'
        

class Test(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=50)
    topic = models.ForeignKey(Topic, verbose_name="Темы", on_delete=models.CASCADE)
    index = models.PositiveIntegerField(default=1, blank=False)
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if Test.objects.filter(topic=self.topic).exists():
            self.index = Test.objects.filter(topic=self.topic).reverse()[0].index + 1
        else:
            self.index = 0
        super().save(*args, **kwargs)
    

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             blank=False, related_name='question_test')
    text = models.CharField(max_length=255, blank=True)
    ANSWER_TYPE_CHOICES = [
        ('c', 'Check box'),
    ]
    type = models.CharField(max_length=1, choices=ANSWER_TYPE_CHOICES,
                            default='с', blank=False)
    score = models.FloatField(default=0.0, blank=False)
    index = models.PositiveIntegerField(blank=False, default=0)
    
    def __str__(self):
        return f'{self.text}'
     

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 blank=False, related_name='answer_test')
    text = models.CharField(max_length=255, blank=True)
    correct_flag = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.text}'
    


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from Profile.models import UserTest, UserTopic
from django.contrib.auth.models import User


@receiver(post_save, sender=Test, dispatch_uid="update_user_test")
def update_user_test(sender, instance, **kwargs):
    if not UserTest.objects.filter(test=instance).exists():
        for user in User.objects.all():
            status = 'з'
            last_compl_test = UserTopic.objects.filter(user=user, topic=instance.topic).reverse()[0].last_completed_test
            if instance.index == 0 or (last_compl_test is not None):
                status = 'о'
            UserTest(
                user=user,
                test=instance,
                status=status,
                last_question=0,
                score=0
            ).save()
    else:
        if instance.index == 0:
            for ut in UserTest.objects.filter(test=instance):
                ut.status = 'о'
                ut.save()
        else:
            for user in User.objects.all():
                for ut in UserTest.objects.filter(test=instance):
                    if UserTopic.objects.filter(user=user, topic=instance.topic).exists():
                        last_compl_test = UserTopic.objects.filter(user=user, topic=instance.topic).reverse()[0].last_completed_test
                    else:
                        last_compl_test = None
                    if last_compl_test is not None:
                        ut.status = 'о'
                    else:
                        ut.status = 'з'
                    ut.save()


@receiver(pre_save, sender=Question, dispatch_uid="update_question")
def update_question(sender, instance, **kwargs):
    instance.index = len(Question.objects.filter(test=instance.test))