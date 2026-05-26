from src.etl.process.extract_dataset import get_dataset_csv
from src.etl.process.transform_dataset import transform_data
from src.etl.process.load_dataset import load

def orchestrator_etl():
    dados = get_dataset_csv("nathansmallcalder/lol-match-history-and-summoner-data-80k-matches")
    transformer = transform_data(dados)
    load(transformer)

if __name__ == "__main__":
    orchestrator_etl()