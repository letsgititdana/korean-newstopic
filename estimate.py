from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaModel
from gensim.test.utils import datapath
import pandas as pd
import os, time, pickle, argparse


parser = argparse.ArgumentParser(description='Script to estimate parameters of LDA and save result files')
parser.add_argument('estimate',
                    choices=['y','n'],
                    help="Whether to fit model. Set as 'y' for the first execution")
parser.add_argument('-c', '--category', metavar='', 
                    choices=['politics', 'society', 'economic', 'culture', 'entertain', 'digital', 'editorial'],
                    help='Information for directory name : caetegory')
parser.add_argument('-s', '--start-date',  metavar='', help='Information for directory name : initial date of publishment')
parser.add_argument('-e', '--end-date',  metavar='', help='Information for directory name : final date of publishment')
parser.add_argument('-k', '--num-topics', type=int, metavar='', help='Number of topics')
parser.add_argument('-na', '--top-na', type=int, metavar='', help='Number of articles to be presented for each topic')
parser.add_argument('-nv', '--top-nv', type=int, metavar='', help='Number of vocabularies to be presented for each topic')
args = parser.parse_args()


def docs_by_topic(model, corpus, topn=20):
    """
    Create dictionary of {topic number:[indices of most relevant documents]}
    """
    triplets = []
    for docidx, doc in enumerate(corpus):
        triplets += [(topic, docidx, proportion) for topic, proportion in model.get_document_topics(doc)]
    parsed_docs = pd.DataFrame(triplets, columns=['topic', 'docidx', 'proportion'])
    return parsed_docs.sort_values(['topic', 'proportion'], ascending=[True, False]).groupby('topic').head(topn)


def vocabs_by_topic(model, dictionary, topn=20):
    """
    Create dictionary of {topic number:[indices of composing words of corresponding topic]}
    """
    triplets = []
    for k in range(model.num_topics):
        topn_vocabs = model.get_topic_terms(k, topn)
        triplets += [(k, dictionary.id2token[vocainfo[0]] , vocainfo[1]) for vocainfo in topn_vocabs]
    return pd.DataFrame(triplets, columns=['topic', 'vocaidx', 'proportion'])


if __name__ == '__main__':

    category = args.category
    start = args.start_date
    end = args.end_date
    n_topics = args.num_topics
    n_articles = args.top_na
    n_vocabs = args.top_nv

    DIR_NAME = os.path.join('./dirs', f"{category}-{start}-{end}")
    with open(os.path.join(DIR_NAME, 'corpus'), 'rb') as f:
        corpus = pickle.load(f)
    dictionary = Dictionary(corpus)
    gensim_corpus = [dictionary.doc2bow(doc) for doc in corpus]


    if args.estimate == 'y':
        print("\nEstimating parameters of LDA model")
        start = time.time()
        model = LdaModel(gensim_corpus, id2word=dictionary, num_topics=n_topics)
        model.save(datapath(f"{category}-{start}-{end}"))
        minute, second = list(map(int, divmod(time.time() - start, 60)))
        print(f">>> Elapsed time : {minute}m {second}s")


    print(f"\nSaving DataFrame of top {n_articles} relevant articles per topic and {n_vocabs} vocabularies from each topic")
    model = LdaModel.load(datapath(f"{category}-{start}-{end}"))
    start = time.time()

    topn_articles = docs_by_topic(model, gensim_corpus, n_articles)
    topn_articles.to_csv(os.path.join(DIR_NAME, 'topn_articles.csv'), index=False)
    with open(os.path.join(DIR_NAME, 'topn_articles'), 'wb') as f:
        pickle.dump(topn_articles, f)

    topn_vocabs = vocabs_by_topic(model, dictionary, n_vocabs)
    topn_vocabs.to_csv(os.path.join(DIR_NAME, 'topn_vocabs.csv'), index=False)
    with open(os.path.join(DIR_NAME, 'topn_vocabs'), 'wb') as f:
        pickle.dump(topn_vocabs, f)

    minute, second = list(map(int, divmod(time.time() - start, 60)))
    print(f">>> Elapsed time : {minute}m {second}s")
    