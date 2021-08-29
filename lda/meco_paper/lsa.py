from pprint import pprint

import plotly.graph_objects as go
from gensim import corpora
from gensim.models import LsiModel, CoherenceModel, LdaModel, TfidfModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 


class Lsa:

    def __init__(self, docs, freq="bow", model="lsi"):

        self.freq = freq
        self.model = model
        self.doc_set = docs

        self.doc_clean = None
        self.dictionary = None
        self.doc_term_matrix = None
        self.topics_count = 2
        self.lsa_model = None

    def best_coherence(self, stop=10, start=3, step=1):
        """
        Input   : dictionary : Gensim dictionary
                  corpus : Gensim corpus
                  texts : List of input texts
                  stop : Max num of topics
        purpose : Compute c_v coherence for various number of topics
        Output  : model_list : List of LSA topic models
                  coherence_values : Coherence values corresponding to the
                  LDA model with respective number of topics
        """

        if self.model == "lsi":
            models = [LsiModel(self.doc_term_matrix,
                               num_topics=n,
                               id2word=self.dictionary)
                      for n in range(start, stop, step)]

        if self.model == "lda":
            models = [LdaModel(self.doc_term_matrix,
                               num_topics=n,
                               id2word=self.dictionary)
                      for n in range(start, stop, step)]

        coherence = [CoherenceModel(model=m,
                                    texts=self.doc_clean,
                                    dictionary=self.dictionary,
                                    coherence="c_v").get_coherence()
                     for m in models]

        d = go.Scatter(x=[i for i in range(start, stop, step)], y=coherence, mode="lines+markers")

        fig = go.Figure()
        fig.add_trace(d)

        fig.update_layout(
            xaxis_title='Topics count',
            yaxis_title='Coherence',
            font=dict(
                family="Times New Roman",
                size=25,
            ),
            legend=dict(
                yanchor="top",
                y=0.98,
                xanchor="right",
                x=0.98
            )
        )
        fig.show()

        max_index = start
        max_score = 0
        for i in range(len(coherence)):
            if max_score < coherence[i]:
                max_index = start + i * step
                max_score = coherence[i]

        self.topics_count = max_index

    def preprocess_data(self):
        """
        Input  : document list
        Purpose: preprocess text (tokenize, removing stopwords, and stemming)
        Output : preprocessed text
        """
        # Initialize regex tokenizer
        tokenizer = RegexpTokenizer(r"\w+")
        # Create English stop words list
        en_stop = set(stopwords.words("english"))
        # Create p_stemmer of class PorterStemmer
        lemmatizer = WordNetLemmatizer()
        # List for tokenized documents in loop
        texts = []
        # Loop through document list
        for i in self.doc_set:
            # Clean and tokenize document string
            raw = i.lower()
            tokens = tokenizer.tokenize(raw)
            # Remove stop words from tokens
            stopped_tokens = [i for i in tokens if i not in en_stop]
            # Stem tokens
            stemmed_tokens = [lemmatizer.lemmatize(i) for i in stopped_tokens]
            # Add tokens to list
            texts.append(stemmed_tokens)

        self.doc_clean = texts

    def prepare_corpus(self):
        """
        Input  : clean document
        Purpose: create term dictionary of our corpus and Converting list of documents (corpus) into Document Term Matrix
        Output : term dictionary and Document Term Matrix
        """
        # Creating the term dictionary of our corpus, where every unique term is
        # Assigned an index. dictionary = corpora.Dictionary(doc_clean)
        self.dictionary = corpora.Dictionary(self.doc_clean)

        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
        self.doc_term_matrix = [self.dictionary.doc2bow(doc)
                                for doc in self.doc_clean]

        if self.freq == "tf-idf":
            tfidf = TfidfModel(self.doc_term_matrix)
            self.doc_term_matrix = tfidf[self.doc_term_matrix]

    def create_lsa_model(self):

        if self.model == "lsi":
            self.lsa_model = LsiModel(self.doc_term_matrix,
                                      num_topics=self.topics_count,
                                      id2word=self.dictionary)

        if self.model == "lda":
            self.lsa_model = LdaModel(self.doc_term_matrix,
                                      num_topics=self.topics_count,
                                      id2word=self.dictionary)
