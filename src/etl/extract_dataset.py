import kagglehub
import os


def get_dataset_csv(dataset: str) -> str:
    return kagglehub.dataset_download(dataset)

path = get_dataset_csv("nathansmallcalder/lol-match-history-and-summoner-data-80k-matches")