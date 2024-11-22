import spacy
from helper import *

# load SpaCy
nlp = spacy.load("en_core_web_sm")

# import our data
df = import_data()

# fetch the first row
# NOTE: Python starts counting at 0, not 1. This means item 0 is the first item in any Python object
row_0 = fetch_row(df, 0)
print_row(row_0)


# TASK: Looking at word POS
doc_0 = nlp(row_0['content'])
print_tokens(doc_0)

# How does tokenizing split up parts of words?
# How does lemmatization change the words?

# TASK: Who are they talking about?
row_1 = fetch_row(df, 1)
print_row(row_1)
doc_1 = nlp(row_1['content'])

# STEP 1: What kind of entities are mentioned in the text (ent.label_)
entity_list = list(set([ent.label_ for ent in doc_1.ents]))
# NOTE: This is an example of a list comprehension, one of Python's most useful data structures. It's basically a mini for-loop used to generate objects.
# NOTE: Lists can have duplicated elements but sets cannot. To de-duplicate entities, we can make the original list into a set and convert back to a list.

# What names can we pull out of one row?
for ent in doc_0.ents:
  print(ent.text, ent.start_char, ent.end_char, ent.label_)

# What names can we pull out of the whole dataset?
for i, row in df.iterrows():
  doc = nlp(row['content'])
  for ent in doc.ents:
    if ent.label_ == "PERSON":
      print(ent.text)









import re
re.sub("\s+", " ", row_0['content']).strip()





for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

for noun_chunk in doc.noun_chunks:
  print(noun_chunk)

doc = nlp(row_0['title'])
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])

doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)


nlp = spacy.load("my_custom_el_pipeline")
doc = nlp("Ada Lovelace was born in London")

# Document level
ents = [(e.text, e.label_, e.kb_id_) for e in doc.ents]
print(ents)  # [('Ada Lovelace', 'PERSON', 'Q7259'), ('London', 'GPE', 'Q84')]

# Token level
ent_ada_0 = [doc[0].text, doc[0].ent_type_, doc[0].ent_kb_id_]
ent_ada_1 = [doc[1].text, doc[1].ent_type_, doc[1].ent_kb_id_]
ent_london_5 = [doc[5].text, doc[5].ent_type_, doc[5].ent_kb_id_]
print(ent_ada_0)  # ['Ada', 'PERSON', 'Q7259']
print(ent_ada_1)  # ['Lovelace', 'PERSON', 'Q7259']
print(ent_london_5)  # ['London', 'GPE', 'Q84']


from spacy.matcher import DependencyMatcher

# "[subject] ... initially founded"
pattern = [
  # anchor token: founded
  {
    "RIGHT_ID": "founded",
    "RIGHT_ATTRS": {"ORTH": "founded"}
  },
  # founded -> subject
  {
    "LEFT_ID": "founded",
    "REL_OP": ">",
    "RIGHT_ID": "subject",
    "RIGHT_ATTRS": {"DEP": "nsubj"}
  },
  # "founded" follows "initially"
  {
    "LEFT_ID": "founded",
    "REL_OP": ";",
    "RIGHT_ID": "initially",
    "RIGHT_ATTRS": {"ORTH": "initially"}
  }
]

matcher = DependencyMatcher(nlp.vocab)
matcher.add("FOUNDED", [pattern])
matches = matcher(doc)
