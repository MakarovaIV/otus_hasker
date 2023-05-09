import json
import os
import re
import shutil

import environ
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import get_connection, EmailMessage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import SignUpForm, \
    QuestionCreateForm, \
    AnswerQuestionForm, \
    CustomUserChangeForm

from .models import Question, Tag, Answer, VoteQuestion, VoteAnswer, CustomUser
from django.conf import settings


env = environ.Env()
environ.Env.read_env()


def get_trending_questions():
    return list(Question.objects.all().order_by('-votes_count', '-creation_date')[:int(env('TRENDING_PAGINATION'))])


class IndexView(ListView):
    model = Question
    success_url = reverse_lazy("login")
    template_name = "hasker_app/index.html"
    context_object_name = 'questions'
    paginate_by = env('INDEX_PAGINATION')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for q in context['questions']:
            q.date = q.creation_date.date()
        context["sort"] = self.request.GET.get('sort', 'hot')
        context["sort_enabled"] = self.request.GET.get('search', '') == ''
        context["search"] = self.request.GET.get('search', '')
        context["trending"] = get_trending_questions()
        return context

    def get_queryset(self):
        search_text = self.request.GET.get('search', '')
        if search_text[:4] == "tag:":
            query = Question.objects.filter(tags__name=search_text[4:])
        elif search_text:
            query = Question.objects.filter(Q(title__contains=search_text) | Q(body__contains=search_text))
        else:
            query = Question.objects.all()

        if self.request.GET.get('sort', 'hot') == 'hot':
            sorted_query = query.order_by('-votes_count', '-creation_date')
        else:
            sorted_query = query.order_by('-creation_date', '-votes_count')
        return sorted_query


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
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
                messages.info(request, f"You are logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, 'Login field is empty')
        else:
            messages.error(request, 'Login or password incorrect')
    form = AuthenticationForm()
    return render(request=request, template_name="hasker_app/login.html", context={"login_form": form})


def logout_handler(request):
    if request.session:
        logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request=request, template_name="hasker_app/logout.html")


def get_user_image(request, pk):
    if request.method == "GET":
        data = CustomUser.objects.filter(id=pk)
        picture_data = list(data)[0].picture_data
        matches = re.match(r".+\.(.+)$", str(list(data)[0].picture))
        extension = matches.group(1) if matches else "jpeg"
        content_type = "image/" + extension
        return HttpResponse(picture_data, content_type=content_type)


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        if hasattr(context["form"], "cleaned_data"):
            for k, v in context["form"].cleaned_data.items():
                context[k] = v
        context["user_id"] = user_id
        context["trending"] = get_trending_questions()
        return context

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'question_id': self.kwargs['question_id']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        tags_str = form.cleaned_data.get("tags_str")
        tags_arr = tags_str.split(",")
        if len(tags_arr) > 3:
            messages.error(self.request, "Should be less than 3 tags")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            q = form.save()
            self.kwargs["question_id"] = q.id
            for tag_str in tags_arr[:3]:
                if tag_str != '':
                    tag, created = Tag.objects.get_or_create(name=tag_str.strip())
                    q.tags.add(tag)
        return super(QuestionCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Form is invalid")
        return self.render_to_response(self.get_context_data(form=form))


class AnswerQuestionView(ListView):
    model = Answer
    form_class = AnswerQuestionForm
    template_name = "hasker_app/answer_form.html"
    context_object_name = 'answers'
    paginate_by = env('ANSWER_PAGINATION')

    def get_queryset(self):
        return Answer.objects.filter(question_id=self.kwargs['question_id']).order_by('-votes_count', '-creation_date')

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'question_id': self.kwargs['question_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        context["question"] = question
        context["user_id"] = self.request.user.id
        try:
            vote_for_question = VoteQuestion.objects.get(question_id=self.kwargs['question_id'],
                                                         user_id=self.request.user.id)
        except:
            vote_for_question = None
        context["vote_for_question"] = vote_for_question
        has_vote_for_question = VoteQuestion.objects.filter(user_id=self.request.user.id)
        context["has_vote_for_question"] = len(has_vote_for_question) > 0
        try:
            vote_for_answer = VoteAnswer.objects.get(question_id=self.kwargs['question_id'],
                                                     user_id=self.request.user.id)
        except:
            vote_for_answer = None
        context["vote_for_answer"] = vote_for_answer
        context["trending"] = get_trending_questions()
        return context


def answer(request):
    if request.method == "POST":
        form = AnswerQuestionForm(request.POST)
        question_id = form.data['question_id']
        if form.is_valid():
            form.instance.user = request.user
            question = get_object_or_404(Question, id=int(question_id))
            form.instance.question = question
            question.answers_count = question.answers_count + 1
            form.save()
            question.save()
            try:
                with get_connection(
                        host=settings.EMAIL_HOST,
                        port=settings.EMAIL_PORT,
                        username=settings.EMAIL_HOST_USER,
                        password=settings.EMAIL_HOST_PASSWORD,
                        use_tls=settings.EMAIL_USE_TLS or False
                ) as connection:
                    subject = "subject"
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [question.user.email]
                    message = format_answer_email(question_id, form.cleaned_data['body'])
                    EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
            except:
                pass
        else:
            messages.error(request, 'Cannot save your answer')
    return HttpResponseRedirect('/question/' + question_id + '/')


def format_answer_email(question_id, answer):
    return """You have new answer
    link to question: {0}
    answer: {1}
    """.format('http://127.0.0.1:8000/question/' + question_id + '/', answer)


def autocomplete_tag(request):
    inputs = request.GET.get('term', ' ').split(",")
    inputs = list(map(lambda tag: tag.strip(), inputs))
    last_input = inputs[-1]
    previous_input = ""
    if len(inputs) > 1:
        previous_input = ", ".join(inputs[:len(inputs) - 1]).strip() + ", "
    tags = Tag.objects.filter(name__contains=last_input.strip())
    results = []
    for tag in tags:
        results.append(previous_input + tag.name)
    data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


def answer_votes(request):
    data = request.POST.copy()
    answer_id = int(data.get("answer_id"))
    question_id = int(data.get("question_id"))
    if request.user.is_authenticated:
        answer = Answer.objects.get(id=answer_id)
        answer_current_count = int(answer.votes_count or 0)
        if data.get("btn_func") == "a_decrement":
            voted_answer = VoteAnswer.objects.filter(question_id=question_id, user_id=request.user.id).first()
            if voted_answer and voted_answer.answer_id == answer_id:
                voted_answer.delete()
                answer.votes_count = answer_current_count - 1
                answer.save()
            else:
                messages.error(request, "You cannot vote")
        elif data.get("btn_func") == "a_increment":
            has_voted_answer = len(VoteAnswer.objects.filter(question_id=question_id, user_id=request.user.id)) > 0
            if has_voted_answer:
                messages.error(request, "You've already voted")
            else:
                vote_answer = VoteAnswer.objects.create(answer_id=answer_id,
                                                        user_id=request.user.id,
                                                        question_id=question_id)
                vote_answer.save()
                answer.votes_count = answer_current_count + 1
                answer.save()
        elif data.get("btn_func") == "set_correct":
            question = get_object_or_404(Question, id=question_id)
            if request.user.id == question.user.id:
                has_correct_answer = len(Answer.objects.filter(question_id=question_id, is_correct=True)) > 0
                if has_correct_answer:
                    messages.error(request, "You've already marked")
                else:
                    answer.is_correct = True
                    answer.save()
            else:
                messages.error(request, "You cannot mark this answer")
        elif data.get("btn_func") == "unset_correct":
            if answer.is_correct:
                answer.is_correct = False
                answer.save()
            else:
                messages.error(request, "You cannot unset")
    return redirect(data['current_path'])


def question_votes(request):
    data = request.POST.copy()
    question_id = int(data.get("question_id"))
    if request.user.is_authenticated:
        question = get_object_or_404(Question, id=question_id)
        question_current_count = int(question.votes_count or 0)
        if data.get("btn_func") == "q_decrement":
            voted_question = VoteQuestion.objects.filter(user_id=request.user.id).first()
            if voted_question and voted_question.question_id == question_id:
                voted_question.delete()
                question.votes_count = question_current_count - 1
                question.save()
            else:
                messages.error(request, "You cannot vote")
        elif data.get("btn_func") == "q_increment":
            has_voted_question = len(VoteQuestion.objects.filter(user_id=request.user.id)) > 0
            if has_voted_question:
                messages.error(request, "You've already voted for question")
            else:
                vote_question = VoteQuestion.objects.create(question_id=question_id, user_id=request.user.id)
                vote_question.save()
                question.votes_count = question_current_count + 1
                question.save()
    return redirect(data['current_path'])


class UserSettings(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, request.FILES)
        data = request.POST.copy()
        if len(data['email']) > 0:
            is_data_changed = False
            if data['email'] != self.request.user.email:
                self.request.user.email = data['email']
                is_data_changed = True
            picture_data = form.files['picture'] if 'picture' in form.files else None
            if picture_data is not None:
                self.request.user.picture_data = picture_data.file.read()
                is_data_changed = True
            if os.path.exists('tmp_upload'):
                shutil.rmtree('tmp_upload')
            if is_data_changed:
                self.request.user.save()
                messages.info(request, "Changes are saved")
        else:
            messages.error(request, "Incorrect email or avatar")
        return render(request, "hasker_app/customuser_form.html")

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)


class UserSettingView(DetailView):
    model = CustomUser
    form_class = CustomUserChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trending"] = get_trending_questions()
        return context


def search_question(request):
    inputs = request.GET.get('term', ' ')
    results = []
    if inputs[:4] == 'tag:':
        tag = inputs[4:]
        tags = Tag.objects.filter(name__startswith=tag.strip())
        for tag in tags:
            results.append("tag:" + tag.name)
    else:
        question = Question.objects.filter(title__contains=inputs) | Question.objects.filter(body__contains=inputs)
        for q in question:
            results.append(q.title)
    data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
