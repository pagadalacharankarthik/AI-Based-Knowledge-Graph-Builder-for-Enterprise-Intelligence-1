from datasets import load_dataset
import pandas as pd

def load_data():
    dataset = load_dataset("corbt/enron-emails")
    df = pd.DataFrame(dataset['train'])
    return df
