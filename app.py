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


# Redirect root to Swagger docs
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


# Optional: Health check endpoint
@app.get("/train")
async def train_route():
    try:
        pass
    except Exception as e:
        raise NetworkSecurityException(e, sys)
