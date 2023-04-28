import json
import os
import re
import shutil

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .forms import SignUpForm, CustomUserCreationForm, QuestionCreateForm, AnswerQuestionForm

from .models import Question, CustomUser, Tag, Answer


class IndexView(ListView):
    model = Question
    success_url = reverse_lazy("login")
    template_name = "hasker_app/index.html"
    context_object_name = 'questions'
    paginate_by = 5


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # login(request, user)

            picture_data = form.cleaned_data['picture']
            default_pic = 'icons/user-profile-icon.png'
            if picture_data is not None:
                user.picture_data = picture_data.file.read()
            else:
                with open(default_pic, 'rb') as data:
                    user.picture_data = data.read()
            user.save()
            if os.path.exists('tmp_upload'):
                shutil.rmtree('tmp_upload')
            return redirect("login")

    else:
        form = SignUpForm()

    return render(request=request,
                  template_name="hasker_app/signup_form.html",
                  context={"form": form})


def login_handler(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="hasker_app/login.html", context={"login_form": form})


def logout_handler(request):
    if request.session:
        logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request=request, template_name="hasker_app/logout.html")


def get_user_image(request):
    if request.method == "GET":
        data = request.user.picture_data
        # reg = re.compile(r".+\.(.+)$")
        matches = re.match(r".+\.(.+)$", str(request.user.picture))
        extension = matches.group(1) if matches else "jpeg"
        content_type = "image/" + extension
        return HttpResponse(data, content_type=content_type)


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.pk
        context["user_id"] = user_id
        return context

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        q = form.save()
        tags_str = form.cleaned_data.get("tags_str")
        tags_arr = tags_str.split(",")
        for tag_str in tags_arr[:3]:
            if tag_str != '':
                tag, created = Tag.objects.get_or_create(name=tag_str.strip())
                q.tags.add(tag)
        return super(QuestionCreateView, self).form_valid(form)


class AnswerQuestionView(CreateView):
    model = Answer
    form_class = AnswerQuestionForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        context["question_title"] = question.title
        context["question_body"] = question.body
        context["question_votes_count"] = question.votes_count
        context["question_tags"] = question.tags
        context["question_id"] = question.id
        context["user_id"] = self.request.user.pk
        answers = Answer.objects.filter(question_id=question.id)

        context["answers"] = list(answers)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = get_object_or_404(Question, id=self.kwargs['question_id'])
        form.save()
        return super(AnswerQuestionView, self).form_valid(form)


def search_tags(request):
    query = request.GET.get('term', '')
    tags = Tag.objects.filter(name__contains=query)
    results = []
    for tag in tags:
        results.append(tag.name)
    data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
