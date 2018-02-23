#from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
#from django.template import loader
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from .models import Question, choice
# Create your views here.
#def index(request):
#    latest_question_list=Question.objects.order_by('-published_date')[:5]
#    template=loader.get_template('ElectionPolls/index.html')
#    context={
#        'latest_question_list':latest_question_list,
#    }
#    return render(request, 'ElectionPolls/index.html', context)

"""code has changed to generic views: Generic view abstract common points so that we dont have to write 
python code to develop an app"""
class IndexView(generic.ListView):
    template_name = 'ElectionPolls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
#views are unchanged: detail, results, votes
#def detail(request, question_id):
#    question=get_object_or_404(Question,pk=question_id)
#    return render(request,'ElectionPolls/detail.html',{'question':question})
#    return HttpResponse('you are looking at the question %s' %question_id)
class DetailView(generic.DetailView):
    model = Question
    template_name = 'ElectionPolls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(published_date__lte=timezone.now())
#def results(request, question_id):
#    question=get_object_or_404(Question,pk=question_id)
#    return render(request,'ElectionPolls/results.html',{'question':question})
#    response='you are looking at the results of the question %s'
#    return HttpResponse(response % question_id)
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'ElectionPolls/results.html'

def votes(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, choice.DoesNotExist):
        return render(request,'ElectionPolls/detail.html',{
            'question':question,
            'error_message':'Your choice is incorrect, please select a valid and correct choice..',
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
#    return HttpResponse('you are voting on question %s' % question_id)