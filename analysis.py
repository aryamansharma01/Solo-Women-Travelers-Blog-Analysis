import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import chardet
import string
files = ['1.csv', '2.csv']


def textnormalizer(s):
    s = s.lower()
    s = re.sub("n’t", " not", s)
    s = re.sub("’re", " are", s)
    s = re.sub("’d be", " would be", s)
    s = re.sub("’d", " had", s)
    s = re.sub("’ll", " will", s)
    s = re.sub("won’t", "will not", s)
    s = re.sub("’s", " is", s)
    s = re.sub("’m", " am", s)
    s = s.replace("…", "")
    s = ''.join([i for i in s if not i.isdigit()])
    # str = str.replace(".", "").replace(",", "").replace("...", "").replace("[", "")
    # str = str.replace("//", "").replace("'", "").replace("")

    # OR {key: None for key in string.punctuation}
    table = str.maketrans(dict.fromkeys(string.punctuation))
    return s.translate(table)


stop_words = set(stopwords.words('english'))


def filter(s):
    s = textnormalizer(s)
    wordlist = s.split()
    s = [w for w in wordlist if w not in stop_words]
    return ' '.join(map(str, s))


def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off")


def vaderanalysis(input):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(input)
    return scores['compound']
    # for key in sorted(scores):
    #    print('{0}: {1}, '.format(key, scores[key]), end='')


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


def frequency(wordstring):
    wordlist = wordstring.split()
    wordfreq = [wordlist.count(w) for w in wordlist]  # a list comprehension

    freq = dict(list(zip(wordlist, wordfreq)))
    return sortFreqDict(freq)


def savefile(text, filename):
    res = frequency(filter(text))

    res = pd.DataFrame(res, columns=['frequency', 'word'])
    res = res[['word', 'frequency']]
    res = res[res.frequency != 1]
    res.to_csv(filename)


input = "My maid Ranya isn't as good as I though she'd be. She'll be removed tomorrow; I don't think she's good enough"
print(filter(input))
print(frequency(filter(input)))

with open('1.csv', 'rb') as f:
    result = chardet.detect(f.readline())

data = pd.read_csv('1.csv')

text = data['paragraphs'].tolist()


for i in range(len(text)):
    df = pd.DataFrame(columns=['S. No', 'Paragraph', 'Sentiment'])
    print("\nCompound: ", vaderanalysis(text[i]))
    text[i] = text[i].split("', '")
    for j in range(len(text[i])):
        df.loc[j] = [j+1, text[i][j], vaderanalysis(text[i][j])]
        #df['S.No'] = j+1
        #df['Paragraph'] = text[i][j]
        #df['Sentiment'] = vaderanalysis(text[i][j])

    df.to_csv(f'BlogSentiment_{i+1}.csv')

# Generate word cloud
wordcloud = WordCloud(width=3000, height=2000, random_state=1, background_color='salmon',
                      colormap='Pastel1', collocations=False, stopwords=STOPWORDS).generate(text[0])
# Plot
plot_cloud(wordcloud)
# wordcloud.to_file("wordcloud.png")

frequency(filter(text[0]))
print(filter(text[0]))
# for i in range(len(text)):
#    savefile(text[i], f'Blog_{i+1}.csv')
