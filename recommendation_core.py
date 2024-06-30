import nltk
from nltk.corpus import stopwords, wordnet as wn 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from operator import itemgetter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


# ^^^^ These imports just to extract keywords from the titles ^^^^


def jacard_calculation(set1: set, set2 :set) -> float:
    """Counts the similarity percentage between two sets

    Args:
        set1 (set): The first set.
        set2 (set): The second set.

    Returns:
        float: The similarity percentage between the two sets.
    """

    inter = set1.intersection(set2)
    return len(inter)/len(set1) if len(set1) != 0 else len(inter)


def ratio_additivity(score: float, likes: int, dislikes: int, views: int) -> float:
    """Takes into account the like/dislike ratio and views

    Args:
        score (float): The initial score.
        likes (int): The number of likes.
        dislikes (int): The number of dislikes.
        views (int): The number of views.

    Returns:
        float: The modified score.
    """

    new_score = 0 if score == 0 else score * 3 + (likes) * .5 + views * .3
    new_score =  score * 3 + (likes/dislikes) * .5 + views * .3 if (dislikes != 0 and score !=0) else new_score
    return new_score


def extract_keywords(sentence) -> list[str]:
    """Takes a sentence and returns a list of the main keywords

    Args:
        sentence (str): The input sentence.

    Returns:
        list[str]: A list of the main keywords extracted from the sentence.
    """

    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.casefold() not in stop_words]
    tagged_words = pos_tag(filtered_words)

    # Reducing the words to infinitive form
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = []
    for word, tag in tagged_words:
        if tag.startswith('NN'):  # Consider only nouns
            pos = wn.NOUN
        elif tag.startswith('VB'):  # Consider only verbs
            pos = wn.VERB
        elif tag.startswith('JJ'):  # Consider only adjectives
            pos = wn.ADJ
        else:
            pos = wn.NOUN
        lemma = lemmatizer.lemmatize(word, pos=pos)
        lemmatized_words.append(lemma)


    # Frequency based calculations
    term_freq = nltk.FreqDist(lemmatized_words)
    sorted_terms = sorted(term_freq.items(), key=itemgetter(1), reverse=True)
    top_keywords = [term for term, freq in sorted_terms[:]]

    #Remove punctuation 
    punctuation = list(".;:?!/\\*+-)(}{)[]'&^¨")
    top_keywords = [term for term in top_keywords if not term in punctuation]

    return top_keywords