from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from DataModel import DataModel
import joblib
import pandas as pd

#TODO hay que agregar la siguiente linea en uvicorn-script.py y el modulos.py en la carpeta de Scripts del env
from modulos import TextWordTokenizer,TextPreprocessor,TextStemLemmatizer,TokensToTextTransformer

app = FastAPI()

# Configurar CORS para permitir solicitudes desde http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ajusta esto según la URL de tu aplicación React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    model = joblib.load('modelo.joblib')
    result = model.predict(df['Textos_espanol'])
    return int(result[0])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    