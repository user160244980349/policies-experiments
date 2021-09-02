import os
from datetime import datetime

from gensim import corpora
from gensim.models import CoherenceModel, LdaModel, TfidfModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from config import resources
from initialization.initialization import initialize


class LDA:

    def __init__(self, docs, freq="bow", topics_count=0, start=2, step=3, stop=30, saved=None):

        initialize()

        self._doc_set = docs
        self._freq = freq

        self._doc_clean = None
        self._dictionary = None
        self._doc_term_matrix = None

        self._preprocess_data()
        self._prepare_corpus()

        if topics_count is None:
            self._topics_count = self._best_coherence(start, step, stop)
        else:
            self._topics_count = 15

        if saved is None:
            self._model = LdaModel(
                self._doc_term_matrix,
                num_topics=self._topics_count,
                id2word=self._dictionary
            )
            self._model.save(os.path.join(resources, f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"))
        else:
            self._model = LdaModel.load(os.path.join(resources, saved))

    def _best_coherence(self, start, step, stop):
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
        models = [LdaModel(self._doc_term_matrix,
                           num_topics=n,
                           id2word=self._dictionary)
                  for n in range(start, stop, step)]

        coherence = [CoherenceModel(model=m,
                                    texts=self._doc_clean,
                                    dictionary=self._dictionary,
                                    coherence="c_v").get_coherence()
                     for m in models]

        # d = go.Scatter(x=[i for i in range(start, stop, step)], y=coherence, mode="lines+markers")
        #
        # fig = go.Figure()
        # fig.add_trace(d)
        #
        # fig.update_layout(
        #     xaxis_title='Topics count',
        #     yaxis_title='Coherence',
        #     font=dict(
        #         family="Times New Roman",
        #         size=25,
        #     ),
        #     legend=dict(
        #         yanchor="top",
        #         y=0.98,
        #         xanchor="right",
        #         x=0.98
        #     )
        # )
        # fig.show()

        max_index = start
        max_score = 0
        for i in range(len(coherence)):
            if max_score < coherence[i]:
                max_index = start + i * step
                max_score = coherence[i]

        return max_index

    def _preprocess_data(self):
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
        for i in self._doc_set:
            # Clean and tokenize document string
            raw = i.lower()
            tokens = tokenizer.tokenize(raw)
            # Remove stop words from tokens
            stopped_tokens = [i for i in tokens if i not in en_stop]
            # Stem tokens
            stemmed_tokens = [lemmatizer.lemmatize(i) for i in stopped_tokens]
            # Add tokens to list
            texts.append(stemmed_tokens)

        self._doc_clean = texts

    def _prepare_corpus(self):
        """
        Input  : clean document
        Purpose: create term dictionary of our corpus and Converting list of documents (corpus) into Document Term Matrix
        Output : term dictionary and Document Term Matrix
        """
        # Creating the term dictionary of our corpus, where every unique term is
        # Assigned an index. dictionary = corpora.Dictionary(doc_clean)
        self._dictionary = corpora.Dictionary(self._doc_clean)

        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
        self._doc_term_matrix = [self._dictionary.doc2bow(doc)
                                 for doc in self._doc_clean]

        if self._freq == "tf-idf":
            tfidf = TfidfModel(self._doc_term_matrix)
            self._doc_term_matrix = tfidf[self._doc_term_matrix]

    def print_topics(self, words=10):
        return self._model.print_topics(
            num_topics=self._model.num_topics,
            num_words=words
        )

    def get_document_topics(self, corpus, minimum_probability):
        return self._model.get_document_topics(
            self._dictionary.doc2bow(corpus),
            minimum_probability=minimum_probability
        )


