import re

text = "Hello!!!  This   is   an Example...   "
print("Original Text:", text)

# Step 1: Clean extra punctuation and spaces
clean_text = re.sub(r'[!?.]+', '.', text)
clean_text = re.sub(r'\s+', ' ', clean_text).strip()
clean_text = clean_text.lower()

print("Cleaned Text:", clean_text)

text = "Hello,world!Let's test:spacing."
print("Before:", text)

spaced_text = re.sub(r'([,.!?;:])', r' \1 ', text)
spaced_text = re.sub(r'\s+', ' ', spaced_text).strip()

print("After:", spaced_text)



print("---------------------------------------------------------------------------------------------------")

from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt_tab')

sentence = "Let's learn tokenization in AI!"
tokens = word_tokenize(sentence)
print("Tokens:", tokens)

print("---------------------------------------------------------------------------------------------------")


from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
text = "Artificial Intelligence revolutionizes industries!"
tokens = tokenizer.tokenize(text)
print("Subword Tokens:", tokens)
