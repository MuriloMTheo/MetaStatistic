import kagglehub
import os


def get_dataset_csv(dataset: str) -> str:
#Etapa responsável pela extração dos dados brutos disponibilizados pelo Kaggle
    return kagglehub.dataset_download(dataset)

path = get_dataset_csv("nathansmallcalder/lol-match-history-and-summoner-data-80k-matches")