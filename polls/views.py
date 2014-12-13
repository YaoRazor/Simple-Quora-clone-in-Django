from django.shortcuts import render, get_object_or_404
from polls.models import Question, Answers
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

logger = logging.getLogger(__name__)


# Create your views here.


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    question_list = Question.objects.order_by('-pub_date')
    paginator = Paginator(question_list, 10)


    page = request.GET.get('page')
    try:
        latest_question_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_question_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_question_list = paginator.page(paginator.num_pages)

    context = {'latest_question_list': latest_question_list, 'username': request.user.username}
    return render(request, 'polls/index.html', context)

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers_set.order_by('-net_votes')
    return render(request, 'polls/detail.html', {'question': question, 'answers': answers})


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers_set.order_by('-net_votes')
    return render(request, 'polls/results.html', {'question': question, 'answers': answers})


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.answers_set.get(pk=request.POST['answer'])
    except (KeyError, Answers.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        if 'VoteUp' in request.POST:
            selected_choice.up_votes += 1
            selected_choice.net_votes = selected_choice.up_votes-selected_choice.down_votes
            print "Up"
        elif 'VoteDown' in request.POST:
            selected_choice.down_votes +=1
            selected_choice.net_votes = selected_choice.up_votes-selected_choice.down_votes
            print "Down"
        else:
            return HttpResponse("Neither Up or Down")

        print request.user

        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

@login_required
def goto_add_page(request):
    return render(request, 'polls/ask.html')


def add_question(request):
    if 'Submit' in request.POST:
        #print "start to create new question"
        new_question_text = request.POST['question_text']
        new_question = Question(question_text=new_question_text, pub_date=timezone.now(), author=request.user)
        new_question.save()
        #print "finish to print new question"
        return HttpResponseRedirect(reverse('polls:index'))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('polls:ask'))
        #print "Cancel"
    else:
        return HttpResponse("Submit new question error")


@login_required
def goto_answer_page(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    context = {'question': p}
    return render(request, 'polls/answer.html', context)


def add_answer(request, question_id):
    if 'Submit' in request.POST:
        p = get_object_or_404(Question, pk=question_id)
        new_answer_text = request.POST['answer_text']
        new_answer = Answers(answer_text=new_answer_text, pub_date=timezone.now(), author=request.user, question=p)
        new_answer.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    else:
        return HttpResponse("Submit new answer error")
