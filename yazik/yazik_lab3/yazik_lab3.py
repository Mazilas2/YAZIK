"""Практическая работа №3"""
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
stopwords = set(stopwords.words('english'))

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function"""
    df = pd.read_csv('youtoxic_english_1000.csv', sep=',', encoding='utf-8')
    df = df[['Text', 'IsToxic', 'IsThreat', 'IsRacist']]
    df = df[(df['IsToxic']) | (df['IsThreat']) | (df['IsRacist'])]
    df['Text'] = df['Text'].str.lower()
    df['Text'] = df['Text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
    df['Text'] = df.apply(lambda row: nltk.word_tokenize(row['Text']), axis=1)
    df['Text'] = df['Text'].apply(lambda x: [word for word in x if word.isalpha()])
    lemmatizer = WordNetLemmatizer()
    df['TextLemmatize'] = df['Text'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
    IsToxicLemma = []
    IsToxic = []
    IsThreatLemma = []
    IsThreat = []
    IsRacistLemma = []
    IsRacist = []
    for i in range(len(df)):
        if df.iloc[i]['IsToxic']:
            IsToxicLemma.extend(df.iloc[i]['TextLemmatize'])
            IsToxic.extend(df.iloc[i]['Text'])
        if df.iloc[i]['IsThreat']:
            IsThreatLemma.extend(df.iloc[i]['TextLemmatize'])
            IsThreat.extend(df.iloc[i]['Text'])
        if df.iloc[i]['IsRacist']:
            IsRacistLemma.extend(df.iloc[i]['TextLemmatize'])
            IsRacist.extend(df.iloc[i]['Text'])
    freqIsToxicLemma = dict(nltk.FreqDist(IsToxicLemma).most_common(20))
    freqIsToxic = dict(nltk.FreqDist(IsToxic).most_common(20))
    freqIsThreatLemma = dict(nltk.FreqDist(IsThreatLemma).most_common(20))
    freqIsThreat = dict(nltk.FreqDist(IsThreat).most_common(20))
    freqIsRacistLemma = dict(nltk.FreqDist(IsRacistLemma).most_common(20))
    freqIsRacist = dict(nltk.FreqDist(IsRacist).most_common(20))
    _, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes[0, 0].barh(list(freqIsToxicLemma.keys()), list(freqIsToxicLemma.values()))
    axes[0, 0].set_title('IsToxicLemma')
    axes[0, 1].barh(list(freqIsToxic.keys()), list(freqIsToxic.values()))
    axes[0, 1].set_title('IsToxic')
    axes[1, 0].barh(list(freqIsThreatLemma.keys()), list(freqIsThreatLemma.values()))
    axes[1, 0].set_title('IsThreatLemma')
    axes[1, 1].barh(list(freqIsThreat.keys()), list(freqIsThreat.values()))
    axes[1, 1].set_title('IsThreat')
    axes[2, 0].barh(list(freqIsRacistLemma.keys()), list(freqIsRacistLemma.values()))
    axes[2, 0].set_title('IsRacistLemma')
    axes[2, 1].barh(list(freqIsRacist.keys()), list(freqIsRacist.values()))
    axes[2, 1].set_title('IsRacist')
    plt.savefig('yazik_lab3.png')
    _, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes[0, 0].imshow(WordCloud().generate_from_frequencies(freqIsToxicLemma))
    axes[0, 0].set_title('IsToxicLemma')
    axes[0, 1].imshow(WordCloud().generate_from_frequencies(freqIsToxic))
    axes[0, 1].set_title('IsToxic')
    axes[1, 0].imshow(WordCloud().generate_from_frequencies(freqIsThreatLemma))
    axes[1, 0].set_title('IsThreatLemma')
    axes[1, 1].imshow(WordCloud().generate_from_frequencies(freqIsThreat))
    axes[1, 1].set_title('IsThreat')
    axes[2, 0].imshow(WordCloud().generate_from_frequencies(freqIsRacistLemma))
    axes[2, 0].set_title('IsRacistLemma')
    axes[2, 1].imshow(WordCloud().generate_from_frequencies(freqIsRacist))
    axes[2, 1].set_title('IsRacist')
    plt.savefig('yazik_lab3_wordcloud.png')


if __name__ == '__main__':
    main()
