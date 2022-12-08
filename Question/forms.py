from django import forms
from Question.models import Answer

class QuestionForm(forms.Form):
    ...
    #text = forms.CharField()
    #answers = forms.MultipleChoiceField()
    
    # def __init__(self, text, choices, type='с', *args, **kwargs):
    #     super (QuestionForm,self ).__init__(*args,**kwargs)
    #     self.fields['text'] = forms.CharField(initial=text, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    #     types = {
    #         'c': forms.CheckboxSelectMultiple(),
    #         'r': forms.RadioSelect()
    #     }
    #     self.fields['answers'] = forms.MultipleChoiceField(choices=choices, widget=types[type])
        
                