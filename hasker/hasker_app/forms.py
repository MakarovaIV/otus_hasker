from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import PasswordInput, EmailInput

from .models import CustomUser, Question, Answer


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "picture"]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "picture"]


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Login', max_length=100)
    email = forms.CharField(label='E-mail', widget=EmailInput, required=True)
    password1 = forms.CharField(label='Password', widget=PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=PasswordInput)
    picture = forms.FileField(label='Avatar', required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "picture"]

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        user_email = CustomUser.objects.filter(email=email)
        if user_email.exists():
            raise forms.ValidationError("Email is existed")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password is not None and password != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data


class QuestionCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    body = forms.CharField(widget=forms.Textarea)
    tags_str = forms.CharField(max_length=100, required=False)
    user_id = forms.IntegerField(required=False)

    class Meta:
        model = Question
        fields = ['title',
                  'body',
                  'tags_str',
                  'user_id']


class AnswerQuestionForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)
    user_id = forms.IntegerField(required=False)
    question_id = forms.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = ['body',
                  'user_id',
                  'question_id']
