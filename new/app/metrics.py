from typing import List
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from jiwer import wer


def compute_rouge(reference: str, prediction: str) -> dict:
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL"], use_stemmer=True
    )
    scores = scorer.score(reference, prediction)

    return {
        "rouge1": scores["rouge1"].fmeasure,
        "rouge2": scores["rouge2"].fmeasure,
        "rougeL": scores["rougeL"].fmeasure,
    }


def compute_bertscore(reference: str, prediction: str) -> float:
    P, R, F1 = bert_score(
        [prediction],
        [reference],
        lang="en",
        verbose=False
    )
    return float(F1.mean())


def compute_wer(reference: str, prediction: str) -> float:
    return wer(reference, prediction)


def evaluate_answer(reference: str, prediction: str) -> dict:
    return {
        "rouge": compute_rouge(reference, prediction),
        "bertscore": compute_bertscore(reference, prediction),
        "wer": compute_wer(reference, prediction),
    }
