from django.http import HttpResponse
from django.shortcuts import render
from .models import Question

# Create your views here.
def index(request):
    # five most recent questions added
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context which provides to template any variables
    context = {
        'latest_question_list': latest_question_list,
    }
    # render template
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    context = {
        'question_id': question_id,
    }
    return render(request,'polls/detail.html', context)

def results(request, question_id):
    return HttpResponse(f'You are looking at the results of question {question_id}')

def vote(request, question_id):
    return HttpResponse(f'You are voting on question {question_id}')
