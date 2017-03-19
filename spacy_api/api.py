import functools
import spacy

nlp_objects = {}

DEFAULT_ATTRIBUTES = ("text", "lemma_", "pos_", "tag_", "vector")


def get_nlp(model="en", embeddings_path=None):
    if embeddings_path not in nlp_objects:
        if embeddings_path is None:
            nlp_ = spacy.load(model)
        else:
            nlp_ = spacy.load(model, vectors=embeddings_path)
        nlp_objects[embeddings_path] = nlp_
    return nlp_objects[embeddings_path]


def json_safety(token, x):
    try:
        value = getattr(token, x)
    except AttributeError:
        print(x, "not found on spacy object")
        value = "ERROR"
    if isinstance(value, (str, int, bool)):
        return value
    else:
        # vectors
        return [float(x) for x in value]


@functools.lru_cache(maxsize=3000000)
def single(document, model="en", embeddings_path=None, attributes=None):
    if attributes is None:
        attributes = DEFAULT_ATTRIBUTES
    nlp_ = get_nlp(model, embeddings_path)
    sentences = []
    for sent in nlp_(document).sents:
        sentence = [{x: json_safety(token, x) for x in attributes}
                    for token in sent]
        sentences.append(sentence)
    return {"sentences": sentences}


def bulk(documents, model="en", embeddings_path=None, attributes=None):
    if attributes is None:
        attributes = DEFAULT_ATTRIBUTES
    parsed_documents = [single(d, model, embeddings_path, attributes) for d in documents]
    return {"documents": parsed_documents}
