import random

import matplotlib.pyplot
import nltk
from nltk.book import *
from nltk.corpus import *
from nltk.corpus import cmudict as jaunt

STOPS = stopwords.words('english')
wordsse = [word.lower() for word in text1 if word.lower() not in STOPS and word.lower().isalpha()]


def c2_e4():
    """
    C2, E4: Read in the texts of the State of the Union addresses, using the state_union corpus reader.
    Count occurrences of men, women, and people in each document.
    What has happened to the usage of these words over time?
    """
    # men, women, gen = 0, 0, 0
    # wordss = state_union.words()
    # for c in wordss:
    #     if c == 'men':
    #         men += 1
    #     if c == 'women':
    #         women += 1
    #     if c == 'people':
    #         gen += 1
    # print('Men:', men, 'Women:', women, 'People:', gen)
    cfd = nltk.ConditionalFreqDist(
        (target, fileid[:4])
        for fileid in state_union.fileids()
        for w in state_union.words(fileid)
        for target in ['men', 'women', 'people']
        if w.lower().startswith(target))
    cfd.plot()


def c2_e5():
    """
    Investigate the holonym-meronym relations for some nouns.
    Remember that there are three kinds of holonym-meronym relation, so you need to use:
    member_meronyms(), part_meronyms(), substance_meronyms(), member_holonyms(), part_holonyms(), and substance_holonyms().
    """
    f, po, pa = wordnet.synset('computer.n.01'), wordnet.synset('people.n.01'), wordnet.synset('paper.n.01')
    print(f.part_meronyms())
    print(f.part_holonyms())
    print(po.member_meronyms())
    print(po.member_holonyms())
    print(pa.substance_meronyms())


def c2_e7():
    """
    According to Strunk and White's Elements of Style, the word however, used at the start of a sentence, means "in whatever way" or "to whatever extent", and not "nevertheless".
    They give this example of correct usage: However you advise him, he will probably do as he thinks best. (http://www.bartleby.com/141/strunk3.html)
    Use the concordance tool to study actual usage of this word in the various texts we have been considering.
    See also the LanguageLog posting "Fossilized prejudices about 'however'" at http://itre.cis.upenn.edu/~myl/languagelog/archives/001913.html
    """
    print("However Concordance:")
    nltk.Text(state_union.words()).concordance("however")


def c2_e9():
    """
    Pick a pair of texts and study the differences between them, in terms of vocabulary, vocabulary richness, genre, etc.
    Can you find pairs of words which have quite different meanings across the two texts, such as monstrous in Moby Dick and in Sense and Sensibility?
    """

    print('1st: The Book of Genisis, 2nd: The Wall Street Journal:')
    print('Meanings of "raise" in The Book of Genisis')
    text3.similar('raise')
    print('Meanings of "raise" in The Wall Street Journal:')
    text7.similar('raise')


def c2_e12():
    """
    The CMU Pronouncing Dictionary contains multiple pronunciations for certain words.
    How many distinct words does it contain?
    What fraction of words in this dictionary have more than one possible pronunciation?
    """
    count_pron, dict_pron, word_pron = 0, jaunt.dict(), jaunt.entries()
    for pair in word_pron:
        pronounciationNumber = len(dict_pron[pair[0]])
        if pronounciationNumber > 1:
            count_pron = count_pron + 1
    print('Distinct Words:', len(dict_pron.keys()))
    print('Multiple Pronounciations:', count_pron)


def c2_e17():
    """
    Write a function that finds the 50 most frequently occurring words of a text that are not stopwords.
    """
    print("50 Greatest Frequency Words (Excluding Stopwords) in Moby Dick:", FreqDist(wordsse).most_common(50))


def c2_e18():
    """
    Write a program to print the 50 most frequent bigrams (pairs of adjacent words) of a text, omitting bigrams that contain stopwords.
    """
    genesisBigrams = nltk.bigrams(text1)
    newGenesisBigrams = list()
    for bi in genesisBigrams:
        stopper = None
        for part in bi:
            if not part.isalpha() or part.lower() in STOPS:
                stopper = True
        if stopper is None:
            newGenesisBigrams.append(bi)
    print('50 Greatest Frequency Bigrams (Excluding Stopwords) in Moby Dick:')
    print(nltk.FreqDist(newGenesisBigrams).most_common(50))


def c2_e23():
    """
    Zipf's Law: Let f(w) be the frequency of a word w in free text. Suppose that all the words of a text are ranked according to their frequency, with the most frequent word first.
    Zipf's law states that the frequency of a word type is inversely proportional to its rank (i.e. f × r = k, for some constant k).
    For example, the 50th most common word type should occur three times as frequently as the 150th most common word type.
    Write a function to process a large text and plot word frequency against word rank using pylab.plot.
    Do you confirm Zipf's law? (Hint: it helps to use a logarithmic scale). What is going on at the extreme ends of the plotted line?
    Generate random text, e.g., using random.choice("abcdefg "), taking care to include the space character.
    You will need to import random first. Use the string concatenation operator to accumulate characters into a (very) long string.
    Then tokenize this string, and generate the Zipf plot as before, and compare the two plots. What do you make of Zipf's Law in the light of this?
    """

    def zipf_plot(text):
        zipf_fre = FreqDist(text)
        pos, hor, ver = 1, list(), list()
        for w in zipf_fre.most_common(len(zipf_fre.keys())):
            frequency = zipf_fre[w[0]]
            hor.append(pos)
            ver.append(frequency)
            pos += 1
        area = 15

        matplotlib.pyplot.scatter(hor, ver, s=area, alpha=.5)
        matplotlib.pyplot.title('ZIFP')
        matplotlib.pyplot.xlabel('Word Rank')
        matplotlib.pyplot.ylabel('Words Frequency')
        matplotlib.pyplot.show()

    zipf_plot(wordsse)
    print("ZIPF PLOT Proves That Word Rank and Frequency Are Inversely Coorelated")


def c2_e27():
    """
    The polysemy of a word is the number of senses it has. Using WordNet, we can determine that the noun dog has 7 senses with: len(wn.synsets('dog', 'n')). Compute the average polysemy of nouns, verbs, adjectives and adverbs according to WordNet.
    """
    s_noun, numSenses = set(), 0
    for synset in list(wordnet.all_synsets(wordnet.NOUN)):
        for e in synset.lemmas():
            if e.name() not in s_noun:
                numSenses = numSenses + len(wordnet.synsets(e.name(), wordnet.NOUN))
                s_noun.add(e.name())
    print('Noun:', numSenses / len(s_noun))

    s_verb, numSenses = set(), 0
    for synset in list(wordnet.all_synsets(wordnet.VERB)):
        for e in synset.lemmas():
            if e.name() not in s_verb:
                numSenses = numSenses + len(wordnet.synsets(e.name(), wordnet.VERB))
                s_verb.add(e.name())
    print('Verb:', numSenses / len(s_verb))

    s_adj, numSenses = set(), 0
    for synset in list(wordnet.all_synsets(wordnet.ADJ)):
        for e in synset.lemmas():
            if e.name() not in s_adj:
                numSenses = numSenses + len(wordnet.synsets(e.name(), wordnet.ADJ))
                s_adj.add(e.name())
    print('Adjective:', numSenses / len(s_adj))

    s_adverb, numSenses = set(), 0
    for synset in list(wordnet.all_synsets(wordnet.ADV)):
        for e in synset.lemmas():
            if e.name() not in s_adverb:
                numSenses = numSenses + len(wordnet.synsets(e.name(), wordnet.ADV))
                s_adverb.add(e.name())
    print('Adverb:', numSenses / len(s_adverb))


def c6_e4():
    """
    Using the movie review document classifier discussed in this chapter, generate a list of the 30 features that the classifier finds to be most informative.
    Can you explain why these particular features are informative? Do you find any of them surprising?
    """

    characteristics = list(nltk.FreqDist(w.lower() for w in movie_reviews.words()))[:2500]

    def establish(document):
        return {'contains({})'.format(w): w in set(document) for w in characteristics}

    documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    featuresets = list()
    for (a, b) in documents:
        featuresets.append((establish(a), b))
    train_set = featuresets[100:]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("30 most important classifier features: ")
    classifier.show_most_informative_features(30)
    print('They are all pretty informative just because they are general blanket statements that can be applied to films. I dont really find any of them all that suprising.')


def main_output():
    print()
    print()
    print('---CHAPTER 2---')

    print()
    print('Problem 4:')
    c2_e4()
    print()

    print()
    print('Problem 5:')
    c2_e5()
    print()

    print()
    print('Problem 7:')
    c2_e7()
    print()

    print()
    print('Problem 9:')
    c2_e9()
    print()

    print()
    print('Problem 12:')
    c2_e12()
    print()

    print()
    print('Problem 17:')
    c2_e17()
    print()

    print()
    print('Problem 18:')
    c2_e18()
    print()

    print()
    print('Problem 23:')
    c2_e23()
    print()

    print()
    print('Problem 27:')
    c2_e27()
    print()

    print()
    print()

    print('---CHAPTER 6---')
    print()
    print('Problem 4:')
    c6_e4()
    print()

    print('Note: had weird url errors on both chapter 3 questions (the ones necessitating url scraping). I think it had to do with my MacOS setup based on what I saw on stack overflow. I ended up skipping those 2 as per the specification on the website/town square.')


c2_e27()
