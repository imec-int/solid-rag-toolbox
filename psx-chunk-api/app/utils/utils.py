import json

from app.models.documents import ChunkType, InputType


def jsonListToStringList(jsonList):
    return [json.dumps(jsonDict) for jsonDict in jsonList]


def validateInputType(inputType):
    if inputType not in InputType:
        return False
    return True


def validateChunkType(chunkType):
    if chunkType not in ChunkType:
        return False
    return True
