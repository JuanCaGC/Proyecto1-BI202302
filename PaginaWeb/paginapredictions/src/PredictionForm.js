import React, { useState } from "react";

function PredictionForm() {
  const [data, setData] = useState({ Textos_espanol: "", sgd: 0 });
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
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
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Textos en español"
          value={data.Textos_espanol}
          onChange={(e) => setData({ ...data, Textos_espanol: e.target.value })}
        />
        <input
          type="number"
          placeholder="sgd"
          value={data.sgd}
          onChange={(e) => setData({ ...data, sgd: e.target.value })}
        />
        <button type="submit">Predict</button>
      </form>
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
