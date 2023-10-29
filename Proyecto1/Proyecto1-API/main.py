from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from io import BytesIO
import os
import tempfile
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



@app.post("/uploadexcel")
async def uploadexcel(excel_file: UploadFile):
    if excel_file.filename.endswith(".xlsx"):
        file_contents = await excel_file.read()
        df = pd.read_excel(BytesIO(file_contents))
        model = joblib.load('modelo.joblib')
        df['Prediction'] = model.predict(df['Textos_espanol'])

        # Create a temporary file to save the Excel data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            temp_filename = temp_file.name
            df.to_excel(temp_filename, sheet_name='Sheet1', index=False)

        # Return the temporary file as a response
        return FileResponse(temp_filename, filename="predicted_data.xlsx")
    else:
        return {"error": "El archivo debe tener la extensión .xlsx"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    