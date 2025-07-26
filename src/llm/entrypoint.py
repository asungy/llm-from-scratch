import requests
import re

url = ("https://raw.githubusercontent.com/rasbt/"
       "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
       "the-verdict.txt")

response = requests.get(url)
text_data = response.text

class SimpleTokenizerV1:
    UNKNOWN = "<unknown>"
    ENDOFLINE = "<endoftext>"

    def __init__(self, raw_data):
        # Preprocessing
        self.re_tokenizer = r'([,.:;?_!"()\']|--|\s)'
        tokenized = re.split(self.re_tokenizer, text_data)
        tokenized = [item.strip() for item in tokenized if item.strip()]
        tokenized.extend([self.UNKNOWN, self.ENDOFLINE])
        
        sorted_tokens = sorted(set(tokenized))
        self.vocab_to_id = {vocab:index for index, vocab in enumerate(sorted_tokens)}
        self.id_to_vocab = {index:vocab for index, vocab in enumerate(sorted_tokens)}
        

    def encode(self, new_text):
        tokenized = re.split(self.re_tokenizer, new_text)
        tokenized = [item.strip() for item in tokenized if item.strip()]
        tokenized = [item if item in self.vocab_to_id else self.UNKNOWN for item in tokenized]
        return [self.vocab_to_id[s] for s in tokenized]

    
    def decode(self, ids):
        text = " ".join([self.id_to_vocab[i] for i in ids]) 
        # Inserting space before the specified puncuation.
        return re.sub(r'\s+([,.?!"()\'])', r'\1', text)

tokenizer = SimpleTokenizerV1(text_data)

text1 = "The quick brown fox jumped over the lazy dog."
text2 = "Jungle asians are cool."
text = SimpleTokenizerV1.ENDOFLINE.join(" ", " ").join((text1, text2))

ids = tokenizer.encode(text)

