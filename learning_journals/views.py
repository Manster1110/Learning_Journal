from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import  reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page"""
    return render(request, 'learning_journals/index.html')

@login_required
def topics(request):
    """Show all the topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_journals/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all associated entries for that topic"""
    topic = Topic.objects.get(id=topic_id)
    # Limit topics to only current owner
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_journals/topic.html', context)

@login_required
def new_topic(request):
    """Add a topic"""
    if request.method != 'POST':
        # No data submitted, so create a blank form
        form = TopicForm()
    else:
        # Data submitted
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_journals:topics'))
    context = {'form': form}
    return render(request, 'learning_journals/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for the topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted
        form = EntryForm()
    else:
        # Data submitted
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_journals:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_journals/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit and existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Pre-fill form with the current entry data
        form = EntryForm(instance=entry)
    else:
        # data submitted, process it
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_journals:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_journals/edit_entry.html', context)