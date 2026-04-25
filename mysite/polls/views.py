from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import hashlib

from .models import Choice, Question, Comment


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
@login_required
def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == "POST":
        text = request.POST.get("text")
        Comment.objects.create(question=question, text=text, user=request.user)
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

def search_questions(request):
    query = request.GET.get('q', '')

    sql = f"SELECT * FROM polls_question WHERE question_text LIKE '%{query}%'"
    questions = Question.objects.raw(sql)
    #Fix:
    #sql = "SELECT * FROM polls_question WHERE question_text LIKE %s"
    #questions = Question.objects.raw(sql, [f"%{query}%"])
    return HttpResponse(questions)

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponse(f'Deleted comment {comment}')
    #Fix
    # if comment.user.id==request.user.id:
    #    comment.delete()
    #    return HttpResponse(f'Deleted comment {comment}')
    #else:
    #    return HttpResponse("Forbidden", status=403)
    
# Create your views here.
