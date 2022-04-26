from urllib.error import HTTPError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import json

from .models import Question
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    return JsonResponse({'result': [model_to_dict(q) for q in latest_questions]})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id);
    choices = question.choice_set.all()
    return JsonResponse({
        'question': model_to_dict(question),
        'choices': [model_to_dict(c) for c in choices]
    })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return JsonResponse({'result': [model_to_dict(c) for c in question.choice_set.all()]})

def vote(request, question_id):
    body = json.loads(request.body)
    choice = body.get('choice')
    question = get_object_or_404(Question, question_id)

    try:
        option = question.choice_set.get(pk=choice)
    except:
        return HttpResponseNotFound({'message': 'Response not found for this question'})
    else:
        option.votes += 1
        option.save()
        return JsonResponse(model_to_dict(option))

