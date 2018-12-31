from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize

people = set()
places = set()

sentence = "Adam Kona: I come from London, United Kingdom."
for sent in sent_tokenize(sentence):
   for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
      if hasattr(chunk, 'label'):
         if chunk.label() == "PERSON":
            person = ' '.join(c[0] for c in chunk)
            people.add(person)
         if chunk.label() == "GPE":
            loc = ' '.join(c[0] for c in chunk)
            places.add(loc)
print(sentence)
print("People: " + str(people))
print("Places: " + str(places))