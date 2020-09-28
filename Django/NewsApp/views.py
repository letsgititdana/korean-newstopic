from django.shortcuts import render
from django.http import HttpResponse
import pickle

def index(request):
    return render(request,'index.html')

def get_vocabs(topn_vocabs):
    vocaidx = []
    for i in range(20):
        vocaidx.append((topn_vocabs.loc[topn_vocabs['topic'] == i]['vocaidx'].values).tolist())
    vocaidx = dict(list(enumerate(vocaidx)))
    return vocaidx

def news2020(request):
    contents = {}
    global year
    global month
    year = '2020'
    month = request.GET.get('month', '')
    if month:
        contents['month'] = month

        link = './NewsApp/static/data/topn_vocabs_' + year + month
        with open(link, 'rb') as f:
            topn_vocabs = pickle.load(f)

        contents['data'] = get_vocabs(topn_vocabs)

    return render(request,'news2020.html', contents)

def news2019(request):
    contents = {}
    global year
    global month
    year = '2019'
    month = request.GET.get('month', '')
    if month:
        contents['month'] = month

        link = './NewsApp/static/data/topn_vocabs_' + year + month
        with open(link, 'rb') as f:
            topn_vocabs = pickle.load(f)

        contents['data'] = get_vocabs(topn_vocabs)
    return render(request,'news2019.html', contents)

def news2018(request):
    contents = {}
    global year
    global month
    year = '2018'
    month = request.GET.get('month', '')
    if month:
        contents['month'] = month

        link = './NewsApp/static/data/topn_vocabs_' + year + month
        with open(link, 'rb') as f:
            topn_vocabs = pickle.load(f)

        contents['data'] = get_vocabs(topn_vocabs)
    return render(request,'news2018.html', contents)

def news2017(request):
    contents = {}
    global year
    global month
    year = '2017'
    month = request.GET.get('month', '')
    if month:
        contents['month'] = month

        link = './NewsApp/static/data/topn_vocabs_' + year + month
        with open(link, 'rb') as f:
            topn_vocabs = pickle.load(f)

        contents['data'] = get_vocabs(topn_vocabs)
    return render(request,'news2017.html', contents)

def articles(request, article_id):
    contents = {}
    contents['id'] = article_id
    contents['year'] = year
    contents['month'] = month

    article_id = int(article_id) - 1

    link2 = './NewsApp/static/data/topn_articles_' + year + month
    with open(link2, 'rb') as f:
        topn_articles = pickle.load(f)

    docidx = (topn_articles.loc[topn_articles['topic'] == article_id]['docidx'].values).tolist()

    link3 = './NewsApp/static/data/titlelist' + year + month + '.txt'
    with open(link3, 'r') as f:
        titlelist = f.read().split('\n')

    link4 = './NewsApp/static/data/urllist' + year + month + '.txt'
    with open(link4, 'r') as f:
        urllist = f.read().split('\n')

    title_list = [titlelist[i] for i in docidx]
    url_list = [urllist[i] for i in docidx]

    dictionary = dict(zip(title_list, url_list))

    contents['data'] = dictionary

    return render(request, 'articles.html', contents)