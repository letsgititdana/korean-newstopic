#from django.contrib.auth.models import User
from django.db import models
from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaModel
from gensim.test.utils import datapath
import pickle, time
import json

# Create your models here.

# class Topic(models.Model):
#     #year = models.IntegerField(null=False, default=2020)
#     #month = models.IntegerField(null=False, default=8)
#     topic1 = models.TextField(null=True)
#     topic2 = models.TextField(null=True)
#     topic3 = models.TextField(null=True)
#     topic4 = models.TextField(null=True)
#     topic5 = models.TextField(null=True)
#     topic6 = models.TextField(null=True)
#     topic7 = models.TextField(null=True)
#     topic8 = models.TextField(null=True)
#     topic9 = models.TextField(null=True)
#     topic10 = models.TextField(null=True)
#     topic11 = models.TextField(null=True)
#     topic12 = models.TextField(null=True)
#     topic13 = models.TextField(null=True)
#     topic14 = models.TextField(null=True)
#     topic15 = models.TextField(null=True)
#     topic16 = models.TextField(null=True)
#     topic17 = models.TextField(null=True)
#     topic18 = models.TextField(null=True)
#     topic19 = models.TextField(null=True)
#     topic20 = models.TextField(null=True)
#

# with open('./NewsApp/static/corpus', 'rb') as f:
#     corpus = pickle.load(f)
#
# dictionary = Dictionary(corpus)
# gensim_corpus = [dictionary.doc2bow(doc) for doc in corpus]
#
# model = LdaModel(gensim_corpus, id2word=dictionary, num_topics=20)
# model.top_topics(gensim_corpus, topn=5)
# top5_words = model.top_topics(gensim_corpus, topn=5)
# top5_list_in_list = [[tuples[1] for tuples in pair[0]] for pair in top5_words]

# Topic().topic1 = json.dumps(top5_list_in_list[0])
# Topic().topic2 = json.dumps(top5_list_in_list[1])
# Topic().topic3 = json.dumps(top5_list_in_list[2])
# Topic().topic4 = json.dumps(top5_list_in_list[3])
# Topic().topic5 = json.dumps(top5_list_in_list[4])
# Topic().topic6 = json.dumps(top5_list_in_list[5])
# Topic().topic7 = json.dumps(top5_list_in_list[6])
# Topic().topic8 = json.dumps(top5_list_in_list[7])
# Topic().topic9 = json.dumps(top5_list_in_list[8])
# Topic().topic10 = json.dumps(top5_list_in_list[9])
# Topic().topic11 = json.dumps(top5_list_in_list[10])
# Topic().topic12 = json.dumps(top5_list_in_list[11])
# Topic().topic13 = json.dumps(top5_list_in_list[12])
# Topic().topic14 = json.dumps(top5_list_in_list[13])
# Topic().topic15 = json.dumps(top5_list_in_list[14])
# Topic().topic16 = json.dumps(top5_list_in_list[15])
# Topic().topic17 = json.dumps(top5_list_in_list[16])
# Topic().topic18 = json.dumps(top5_list_in_list[17])
# Topic().topic19 = json.dumps(top5_list_in_list[18])
# Topic().topic20 = json.dumps(top5_list_in_list[19])
# Topic().save()