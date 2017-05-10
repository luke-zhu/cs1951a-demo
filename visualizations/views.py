import datetime
from django.shortcuts import render
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from django.utils.datastructures import MultiValueDictKeyError

from .models import RedditPost, GeniusPost


# Create your views here.
def home(request):
    return render(request, 'visualizations/home.html')

def reddit(request, q1='', q2 = '', q3=''):
    if request.GET.get('q1')is not None:
        q1 = request.GET.get('q1')
    if request.GET.get('q2') is not None:
        q2 = request.GET.get('q2')
    if request.GET.get('q3')is not None:
        q3 = request.GET.get('q3')
    reddit_posts = serialize('json', RedditPost.objects.all(), cls=DjangoJSONEncoder)
    context = {'title': 'r/hiphopheads Time Series',
    'posts': reddit_posts, 'q1': q1, 'q2': q2, 'q3': q3}
    return render(request, 'visualizations/reddit.html', context)

def genius(request, q1='', q2='', q3=''):
    if request.GET.get('q1') is not None:
        q1 = request.GET.get('q1')
    if request.GET.get('q2') is not None:
        q2 = request.GET.get('q2')
    if request.GET.get('q3') is not None:
        q3 = request.GET.get('q3')
    start_date = datetime.datetime(2016, 1, 2)
    end_date = datetime.datetime(2017, 5, 1)
    genius_posts = serialize('json', GeniusPost.objects \
        .filter(datetime__lt=end_date, datetime__gte=start_date),
        cls=DjangoJSONEncoder);
    context = {'title': 'RapGenius Time Series', 
    'posts': genius_posts, 'q1': q1, 'q2': q2, 'q3': q3}
    return render(request, 'visualizations/reddit.html', context)

