from django import forms
from .models import Question, Reply

class QuestionInlineForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'thread': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'question': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'answer': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'timestamp': forms.Textarea(attrs={'rows': 2, 'cols': 17}),
        }

class ReplyInlineForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'timestamp': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        }
