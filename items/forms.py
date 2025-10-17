from django import forms
from .models import LostItem, FoundItem, VerificationQuestion
from .models import ClaimAttempt

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['item_name', 'description', 'photo', 'location', 'date_found']


class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['item_name', 'description', 'photo', 'location', 'date_lost']


class VerificationQuestionForm(forms.ModelForm):
    class Meta:
        model = VerificationQuestion
        fields = ['question_text', 'answer']

class ClaimAttemptForm(forms.ModelForm):
    class Meta:
        model = ClaimAttempt
        fields = ['answer1', 'answer2', 'answer3']
        widgets = {
            'answer1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter answer'}),
            'answer2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter answer'}),
            'answer3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter answer'}),
        }