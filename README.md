## spacy_api

Helps with loading models in a separate, dedicated process.

Caching happens on unique arguments.

#### Features

- ✓ Serve models separately
- ✓ Client- and Server-side caching
- ✓ CLI interface

### Install

Should work with py2 and py3.

Install on a machine that will run both client and server:

    pip install spacy_api[all]

Server only (spacy, mprpc):

    pip install spacy_api[server]

Client Only (numpy, mprpc):

    pip install spacy_api[client]

### Example

Run the server:

    spacy serve

Then open a python process and run code in the next section.

#### Single document

```python
from spacy_api import Connector

spacy_client = Connector() # default args host/port

doc = spacy_client.single("How are you")
doc
# [[How, are, you]]

# iterate over sentences
for sentence in doc.sents:
    for token in sentence:
        print(token.text, token.pos_, token.lemma_)

# iterate over a whole document
for token in doc:
    print(token)
```

#### Switch to running spacy within the process

Instead of

    from spacy_api import Connector

use

    from spacy_api import LocalConnector

#### Arguments

```python
# language/model
doc = spacy_client.single("How are you", model="en")

# Using google pretrained vectors
doc = spacy_client.single("How are you", embeddings_path="en_google")

# Tell spacy which attributes to give back, comma separated
doc = spacy_client.single("How are you", attributes="text,lemma_,pos,vector")
```

Naturally, you can use any combination of these.

#### Bulk of documents

```python
docs = spacy_client.bulk(["How are you"]*100)
for doc in docs:
    for sentence in doc.sents:
        for token in sentence:
            print(token.text, token.pos_, token.lemma_)

```
