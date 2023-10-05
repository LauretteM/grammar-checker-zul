import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Download NLTK data
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

def tokenize_and_tag(input_text):
    # Tokenize the input text into sentences
    sentences = sent_tokenize(input_text)
    
    # Tokenize each sentence into words
    tokenized_and_tagged_text = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words) # perform part-of-speech tagging
        tokenized_and_tagged_text.append(pos_tags)
    
    return tokenized_and_tagged_text

# Example
input_text = "IsiZulu siyisifiso sezulu esikhulu esikwazi ukubamba iqhaza likaMoya. Lokhu kusiza abantu ukwazi ukuthandaza noma ukuziphendula imithandazo yabo ngokucophelela. Izikhathi eziningi, izulu lisendaweni efudumele kwangaphambili kwesizukulwane sasemhlabeni."
tokenized_and_tagged_text = tokenize_and_tag(input_text)
print(tokenized_and_tagged_text)
