import React, { useState } from "react";

function PredictionForm() {
  const [textosEspanol, setTextosEspanol] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handlePredictClick = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ Textos_espanol: textosEspanol }),
      });

      if (response.ok) {
        const result = await response.json();
        setPrediction(result);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Textos en español"
        value={textosEspanol}
        onChange={(e) => setTextosEspanol(e.target.value)}
      />
      <button onClick={handlePredictClick}>Predict</button>
      {prediction !== null && (
        <div>
          <h3>Prediction Result:</h3>
          <p>{prediction}</p>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;
