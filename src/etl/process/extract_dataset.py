import kagglehub

def get_dataset_csv(dataset: str) -> str:
#Etapa responsável pela extração dos dados brutos disponibilizados pelo Kaggle
    dataset_extract = kagglehub.dataset_download(dataset)
    return dataset_extract