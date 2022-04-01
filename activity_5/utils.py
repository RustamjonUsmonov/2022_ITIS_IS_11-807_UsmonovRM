import math
import pickle

import pymorphy2
from typing import Dict, List

site_db_filename = "../activity_3/sites_db.pickle"
lemma_base_vector_db_name = "lemma_base_vector_db.pickle"
idf_global_lemmas_db_name = "idf_global_lemmas.pickle"
vectors_by_doc_db_name = "vectors_by_doc_db.pickle"


def get_lemma_from_token(token: str) -> str:
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(token)[0]
    return p.normal_form


def text_preprocessing(input_text: str) -> str:
    # убираем знаки пунктуации и числа; приводим к нижнему регистру
    punctuation = """!"#$%&\'()*+,.:;<=>?@[\\]^_`{|}~"""
    tt = str.maketrans(dict.fromkeys(f"{punctuation}“”«»"))
    return input_text.lower().translate(tt).replace("/", " ")


def get_sites() -> Dict[int, str]:
    with open(site_db_filename, 'rb') as sites_db:
        sites = pickle.load(sites_db)
    return sites


def get_base_vector() -> Dict[str, float]:
    with open(lemma_base_vector_db_name, 'rb') as vector:
        base_vector = pickle.load(vector)
    return base_vector


def get_global_idf_lemmas() -> Dict[str, float]:
    with open(idf_global_lemmas_db_name, 'rb') as f:
        idf_lemmas = pickle.load(f)
    return idf_lemmas


def get_vectors_by_doc() -> Dict[int, List[float]]:
    with open(vectors_by_doc_db_name, 'rb') as f:
        vectors = pickle.load(f)
    return vectors


def cos(v1: List[float], v2: List[float]) -> float:
    # косинусная мера между векторами
    sum_numerator = sum(list(map(lambda el: el[0] * el[1], zip(v1, v2))))

    len_v1 = math.sqrt(sum(map(lambda x: x * x, v1)))
    len_v2 = math.sqrt(sum(map(lambda x: x * x, v2)))
    denominator = len_v1 * len_v2
    if denominator == 0:
        return 0
    return sum_numerator / denominator
