from django import forms
from .models import Question

class QuestionInlineForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'question': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'answer': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
