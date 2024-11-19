from textwrap import wrap


def chunkOnTokens(documents, chunkSize):
    chunks = []
    for document in documents:
        chunks.append(wrap(document, chunkSize))
    return chunks


def chunkOnSentences(documents):
    chunks = []
    for document in documents:
        split = [str(item.strip()) for item in document.split(".") if item != ""]
        chunks.append(split)
    return chunks


def chunkOnParagraphs(documents):
    chunks = []
    for document in documents:
        split = [str(item.strip()) for item in document.splitlines() if item != ""]
        chunks.append(split)
    return chunks
