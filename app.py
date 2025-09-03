import sys
import os
import certifi
import pymongo
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import load_object

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Setup MongoDB client with TLS
ca = certifi.where()
try:
    client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
    client.admin.command("ping")
    logging.info("MongoDB connection established.")
except Exception as e:
    raise NetworkSecurityException(e, sys) from e

# Access database and collection
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Template configuration
templates = Jinja2Templates(directory="./templates")  # ✅ Use relative path


# Redirect root to Swagger docs
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


# Training route
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(
            content="Training has been successfully completed", media_type="text/plain"
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)


# Prediction route
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        print(df.head())
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(
            preprocessor=preprocessor, model=final_model
        )  # ✅ Fixed typo
        y_pred = network_model.predict(df)

        df["predicted_column"] = y_pred
        df.to_csv("prediction_output/output.csv", index=False)

        table_html = df.to_html(classes="table table-striped", index=False)
        return templates.TemplateResponse(
            "table.html", {"request": request, "table": table_html}
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)


# Run the app
if __name__ == "__main__":
    from uvicorn import run as app_run

    app_run(app, host="localhost", port=8000)
