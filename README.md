# House Price Prediction

A machine learning web app that predicts house prices for Delhi, Gurgaon, and Meerut markets.

## Project Structure

```
house-price-prediction/
├── data/
│   ├── raw/house_data.csv
│   ├── processed/
│   └── generate_data.py
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   └── evaluate_model.py
├── models/                  # Trained model artifacts
├── app/
│   ├── app.py               # Flask app
│   └── templates/index.html
├── notebooks/eda.ipynb
├── run_pipeline.py
└── requirements.txt
```

## Setup & Run

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Generate data & train model**
```bash
python data/generate_data.py
python run_pipeline.py
```

3. **Start the web app**
```bash
cd app
python app.py
```

Open: [http://localhost:5000](http://localhost:5000)

## API

`POST /api/predict`

```json
{
  "area": 1200,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 5,
  "location_score": 7.5,
  "city": "Delhi"
}
```

Response:
```json
{ "success": true, "prediction": 8500000, "formatted": "Rs 8,500,000" }
```
