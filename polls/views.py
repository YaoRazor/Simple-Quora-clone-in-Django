from django.shortcuts import render, get_object_or_404
from polls.models import Question, Answers, Tags
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone, feedgenerator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging


logger = logging.getLogger(__name__)


# Create your views here.

def tag_handler(request, tag_id):
    tag = get_object_or_404(Tags, pk=tag_id)
    question_list = sorted(tag.question_set.all(), key=lambda x: x.pub_date,
                           reverse=True)
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

    context = {'latest_question_list': latest_question_list, 'username': request.user.username,
               'tag': tag.tag}
    return render(request, 'polls/index.html', context)



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

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers_set.order_by('-net_votes')
    return render(request, 'polls/detail.html', {'question': question, 'answers': answers,
    'username': request.user.username, 'taglist':question.tags.all}, )


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers_set.order_by('-net_votes')
    return render(request, 'polls/results.html', {'question': question, 'answers': answers})


def question_vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    # Deal with question vote
    if 'VoteUpQuestion' in request.POST:
        if request.user not in p.up_list.all():
            p.up_list.add(request.user)
            p.up_votes += 1

    elif 'VoteDownQuestion' in request.POST:
        if request.user not in p.down_list.all():
            p.down_list.add(request.user)
            p.down_votes += 1

    # update database for question
    p.save()

    # Deal with question vote


@login_required
def vote(request, question_id):
    if 'VoteUpQuestion' in request.POST or 'VoteDownQuestion' in request.POST:
        question_vote(request, question_id)
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))

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


        # Deal with answer vote
        if 'VoteUp' in request.POST:
            # check if duplicate vote, guarantee one user can only vote up once
            if request.user not in selected_choice.up_list.all():
                selected_choice.up_list.add(request.user)
                selected_choice.up_votes += 1

            selected_choice.net_votes = selected_choice.up_votes-selected_choice.down_votes
        elif 'VoteDown' in request.POST:
            # check if duplicate vote, guarantee one user can only vote down once
            if request.user not in selected_choice.down_list.all():
                selected_choice.down_list.add(request.user)
                selected_choice.down_votes += 1

            selected_choice.net_votes = selected_choice.up_votes-selected_choice.down_votes
        # Deal with answer vote

        # update database for answers
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:detail', args=(p.id,)))

@login_required
def goto_add_page(request):
    context = {'username': request.user.username}
    return render(request, 'polls/ask.html', context)


def add_question(request):
    if 'Submit' in request.POST:
        new_question_title = request.POST['question_title']
        new_question_text = request.POST['question_text']
        new_question = Question(question_text=new_question_text, pub_date=timezone.now(), author=request.user,
                                modification_time=timezone.now(), question_title=new_question_title)
        tag_string = request.POST['tags']
        tags = tag_string.split(',')

        new_question.save()
        for new_tag in tags:
            new_tag_object = Tags(tag=new_tag)
            #new_tag_object.save()
            if Tags.objects.filter(tag=new_tag):
                new_question.tags.add(Tags.objects.get(tag=new_tag))
            else:
                #print "not exists"
                #print Tags.objects.get(tag=new_tag)
                # print Tags.objects.get(tag=new_tag)
                # new_tag_object = Tags.objects.get(tag=new_tag)
                # print "get successfully"
                # new_question.tags.add(new_tag_object)
                # print "add successfully"
                new_tag_object.save()
                new_question.tags.add(new_tag_object)

        print "out of for"
        new_question.save()

        #print new_question.tags.all()
        return HttpResponseRedirect(reverse('polls:index'))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('polls:ask'))
    else:
        return HttpResponse("Submit new question error")


@login_required
def goto_answer_page(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    context = {'question': p, 'username': request.user.username}
    return render(request, 'polls/answer.html', context)


def add_answer(request, question_id):
    if 'Submit' in request.POST:
        p = get_object_or_404(Question, pk=question_id)
        new_answer_text = request.POST['answer_text']
        new_answer = Answers(answer_text=new_answer_text, pub_date=timezone.now(), author=request.user, question=p,
                             modification_time=timezone.now())
        new_answer.save()
        p.number_of_answers = len(p.answers_set.all())
        p.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    else:
        return HttpResponse("Submit new answer error")

@login_required
def edit_question_page(request, question_id):
    p = get_object_or_404(Question, pk=question_id)

    can_edit = False
    if request.user == p.author:
        can_edit = True

    context = {'question': p, "can_edit": can_edit}
    return render(request, 'polls/edit_question_page.html', context)


def edit_question(request, question_id):
    if 'Submit' in request.POST:
        p = get_object_or_404(Question, pk=question_id)
        p.question_text = request.POST['question_text']
        p.question_title = request.POST['question_title']
        p.modification_time = timezone.now()
        p.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    else:
        return HttpResponse("Submit new answer error")

@login_required
def edit_answer_page(request, question_id, answer_id):
    p = get_object_or_404(Answers, pk=answer_id)
    q = get_object_or_404(Question, pk=question_id)

    can_edit = False
    if request.user == p.author:
        can_edit = True

    context = {'answer': p, "can_edit": can_edit, 'question': q}
    return render(request, 'polls/edit_answer_page.html', context)


def edit_answer(request, question_id, answer_id):
    if 'Submit' in request.POST:
        p = get_object_or_404(Answers, pk=answer_id)
        p.answer_text = request.POST['answer_text']
        p.modification_time = timezone.now()
        p.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    else:
        return HttpResponse("Submit new answer error")


def rss(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers_set.order_by('-net_votes')
    # create a feed generator having a channel with following title, link and description
    # feed = feedgenerator.Rss201rev2Feed(
    #     title=question.question_title,
    #     content=question.question_text,
    # )
    feed = feedgenerator.Rss201rev2Feed(
        title="Output question rss",
        link="",
        description=u"This is the content of all staff related to one question.",
        language=u"en",
    )

    feed.add_item(
        title=question.question_title,
        link=u"",
        description=question.question_text)

    for answer in answers:
        feed.add_item(
            title=u"answer",
            link="",
            description=answer.answer_text,)
            #up_votes=str(answer.up_votes),

    # Write all the feeds in a string
    str=feed.writeString('utf-8')
    # You can use following to write the same in a file
    #with open('test.rss', 'w') as fp:
    #	feed.write(fp, 'utf-8')

    # format the string so that it will be readable
    context = {}
    str = format(str)
    context['str'] = str

    return render(request, 'polls/rss.html', context)

def format(str):
    str=str.replace('>', '>\n')
    str=str.replace('<', '\n<')
    str=str.replace('\n\n', '\n')
    return str
