from django.http import HttpResponse
from .models import Question

# Create your views here.
def index(request):
    question_list = Question.objects.all()
    question_list_parsed = ', '.join([q.question_text for q in question_list])
    return HttpResponse(f'Most recent questions: {question_list_parsed}')

def detail(request, question_id):
    return HttpResponse(f'You are looking at question {question_id}')

def results(request, question_id):
    return HttpResponse(f'You are looking at the results of question {question_id}')

def vote(request, question_id):
    return HttpResponse(f'You are voting on question {question_id}')
