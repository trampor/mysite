from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from .models import Question,Choice
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def index(request):
    latest_question_list=Question.objects.all()
    print(latest_question_list)
    context={'latest_question_list':latest_question_list}
    return render(request,'polls/index.html',context)
    template=loader.get_template('polls/index.html')
    return HttpResponse(template.render(context,request))

def detail(request,question_id):
#    try:
#        question=Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':'you do not select a choice',})
    else:
        choice.votes+=1;
        choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
