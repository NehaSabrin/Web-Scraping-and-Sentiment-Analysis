import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import SyllableTokenizer

def extract_article_text(url):
 # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object from the response content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the article title
    article_title = soup.find('h1').text.strip()

    # Find the article element by its CSS selector or XPath
    article = soup.select_one('.td-post-content')

    # Remove unwanted sections
    unwanted_sections = ['header', 'footer', '.td-related-right', '.td-popular-right', '.td-comments-title',
                         '.td-post-sharing-top']
    for section in unwanted_sections:
        if section.startswith('.'):
            for element in article.select(section):
                element.extract()
        else:
            unwanted_element = article.find(section)
            if unwanted_element:
                unwanted_element.extract()

    # Extract the text from the remaining article
    article_text = article.get_text(separator='\n')

    return article_title, article_text.strip()

def calculate_metrics(text):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Calculate the positive score and negative score
    positive_score = sum(1 for word in words if TextBlob(word).sentiment.polarity > 0)
    negative_score = sum(1 for word in words if TextBlob(word).sentiment.polarity < 0)


    # Calculate the average sentence length
    avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)

    # Calculate the percentage of complex words
    stop_words = set(stopwords.words('english'))
    complex_word_count = 0
    total_word_count = 0
    lemmatizer = WordNetLemmatizer()
    for word in words:
        if word.lower() not in stop_words:
            total_word_count += 1
            lemma = lemmatizer.lemmatize(word)
            if len(lemma) > 2 and lemma.isalpha():
                complex_word_count += 1
    percentage_complex_words = (complex_word_count / total_word_count) * 100

    # Calculate the Fog index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Calculate the average number of words per sentence
    avg_words_per_sentence = len(words) / len(sentences)

    # Calculate the number of personal pronouns
    personal_pronouns = ['I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
    personal_pronoun_count = sum(word.lower() in personal_pronouns for word in words)

    # Calculate the average word length
    avg_word_length = sum(len(word) for word in words) / len(words)

    # Calculate the number of personal pronouns
    personal_pronouns = ['I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
    personal_pronoun_count = sum(word.lower() in personal_pronouns for word in words)
    
    # Calculate the average word length
    avg_word_length = sum(len(word) for word in words) / len(words)

    # Calculate sentiment scores
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity

    # Classify sentiment as positive or negative
    if polarity_score > 0:
        sentiment = "Positive"
    elif polarity_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Calculate syllables per word
    syllable_tokenizer = SyllableTokenizer()
    syllables_per_word = sum(len(syllable_tokenizer.tokenize(word)) for word in words) / len(words)

    # Return all the calculated metrics
    return polarity_score, subjectivity_score, positive_score, negative_score,avg_sentence_length, percentage_complex_words, fog_index, \
           avg_words_per_sentence, complex_word_count, total_word_count, personal_pronoun_count, \
           avg_word_length, syllables_per_word, personal_pronoun_count, avg_word_length, sentiment

# Example usage
url = "https://example.com/"
article_title, article_text = extract_article_text(url)
(polarity_score, subjectivity_score, positive_score, negative_score, avg_sentence_length, percentage_complex_words, fog_index,
 avg_words_per_sentence, complex_word_count, total_word_count, personal_pronoun_count,
 avg_word_length, syllables_per_word, personal_pronoun_count, avg_word_length, sentiment) = calculate_metrics(article_text)

print("Article Title:", article_title)
print("Article Text:", article_text)
print("Positive Score:", positive_score)
print("Negative Score:", negative_score)
print("Polarity Score:", polarity_score)
print("Subjectivity Score:", subjectivity_score)
print("Average Sentence Length:", avg_sentence_length)
print("Percentage of Complex Words:", percentage_complex_words)
print("Fog Index:", fog_index)
print("Average Words per Sentence:", avg_words_per_sentence)
print("Complex Word Count:", complex_word_count)
print("Word Count:", total_word_count)
print("Syllables per Word:", syllables_per_word)
print("Personal Pronouns Count:", personal_pronoun_count)
print("Average Word Length:", avg_word_length)
print("Sentiment:", sentiment)
