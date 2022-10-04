from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.retriever.sparse import TfidfRetriever
from haystack.pipeline import ExtractiveQAPipeline
from haystack.document_store.memory import InMemoryDocumentStore
import pandas as pd

def elastic_search(text_to_search):
  document_store = InMemoryDocumentStore()
  doc_dir = "uploads"
  dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)

  print(dicts[:3])
  document_store.write_documents(dicts)

  retriever = TfidfRetriever(document_store=document_store)

  reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

  pipe = ExtractiveQAPipeline(reader, retriever)
  prediction = pipe.run(query=text_to_search, top_k_retriever=10, top_k_reader=5)

  df = prediction['answers']
  answers = []
  contexts = []
  names = []
  scores = []

  for i in range(5):
    answers.append(df[i]['answer'])
    contexts.append(df[i]['context'])
    names.append(df[i]['meta']['name'])
    scores.append(df[i]['score']*100)

  data = pd.DataFrame()
  data['answers'] = answers
  data['contexts'] = contexts
  data['names'] = names
  data['scores'] = scores
  data.reset_index(inplace=True)
  data.to_csv("data.csv",index=False)
  return data