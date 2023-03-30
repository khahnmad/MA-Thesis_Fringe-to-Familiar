from pydantic import BaseModel
from typing import List, Dict
from pydantic.error_wrappers import ValidationError
import tensorflow as tf

class SRO_Instance(BaseModel):
    subject: str
    subjectSpan: List[int]
    relation: str
    relationSpan: List[int]
    object: str
    objectSpan: List[int]
    tokenized_sentence: List[str]
    sentence_id: int
    article_id: str
    entity_location: dict


class Sentiment_Instance(BaseModel):
    subject: str
    subjectSpan: List[int]
    relation: str
    relationSpan: List[int]
    object: str
    objectSpan: List[int]
    tokenized_sentence: List[str]
    sentence_id: int
    article_id: str
    entity_location: dict
    sentiment : int


class OpenIEResponse(BaseModel):
    subject: str
    subjectSpan: List[int]
    relation : str
    relationSpan: List[int]
    object: str
    objectSpan: List[int]


class SentenceResponse(BaseModel):
    index: int
    basicDependencies : List[dict]
    enhancedDependencies : List[dict]
    enhancedPlusPlusDependencies : List[dict]
    openie: List[OpenIEResponse]
    entitymentions : List[dict] # TODO : could make another class for this
    tokens : List[dict]


class StanfordModelResponse(BaseModel):
    sentences: List[SentenceResponse]
    corefs: Dict

class EmbeddingTriplet(BaseModel):
    subject: str
    subjectSpan: List[int]
    relation: str
    relationSpan: List[int]
    object: str
    objectSpan: List[int]
    tokenized_sentence: List[str]
    sentence_id: int
    article_id: str
    entity_location: dict
    embedding: tf.Variable
    # sentiment: Optional[int]
    class Config:
        arbitrary_types_allowed = True

