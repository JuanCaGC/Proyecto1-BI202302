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
    model = load('modelo.joblib')
    result = model.predict(df['Textos_espanol'])
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    