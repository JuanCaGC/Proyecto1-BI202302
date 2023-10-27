from DataModel import DataModel
from joblib import load
from typing import Union
import pandas as pd
from fastapi import FastAPI

app = FastAPI()


@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    model = load(r'.\Proyecto1\modelo.joblib')
    result = model.predict(df)
    return result
