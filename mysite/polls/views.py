from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
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
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    return HttpResponse(f'You are looking at the results of question {question_id}')

def vote(request, question_id):
    return HttpResponse(f'You are voting on question {question_id}')
