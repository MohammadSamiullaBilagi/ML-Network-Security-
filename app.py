# import sys
# import os

# import certifi
# ca=certifi.where()

# from dotenv import load_dotenv
# load_dotenv()
# mongo_db_url=os.getenv("MONGODB_URL_KEY")
# print(mongo_db_url)

# import pymongo

# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging
# from networksecurity.pipeline.training_pipeline import TrainingPipeline
# from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI,File,UploadFile,Request
# from uvicorn import run as app_run
# from fastapi.responses import Response
# from starlette.responses import RedirectResponse
# import pandas as pd

# from networksecurity.utils.main_utils.utils import load_object


# client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

# from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
# from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME

# database=client[DATA_INGESTION_DATABASE_NAME]
# collection=database[DATA_INGESTION_COLLECTION_NAME]


# app=FastAPI()
# origins=["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# from fastapi.templating import Jinja2Templates
# templates=Jinja2Templates(directory="./templates")

# @app.get("/",tags=["authentication"])
# async def index():
#     return RedirectResponse(url="/docs")


# @app.get("/train")
# async def train_route():
#     try:
#         train_pipeline=TrainingPipeline()
#         train_pipeline.run_pipeline()
#         return Response("Training is successfull")
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)

# @app.get("/predict")
# async def predict_route(request:Request,file:UploadFile=File(...)):
#     try:
#         df=pd.read_csv(file.file)
#         preprocessor=load_object("final_model/preprocessor.pkl")
#         final_model=load_object("final_model/model.pkl")
#         network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
#         print(df.iloc[0])
#         y_pred=network_model.predict(df)
#         print(y_pred)
#         df['predicted_column']=y_pred
#         print(df['predicted_column'])
#         df.to_csv("prediction_data/output.csv")
#         table_html=df.to_html(classes='table table-striped')
#         return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)
    
# if __name__=="__main__":
#     app_run(app,host="localhost",port=8000)

# app.py (patched)

import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, status
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successfull")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


# <-- FIXED: use POST for file upload -->
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # read uploaded CSV into DataFrame
        df = pd.read_csv(file.file)

        # Attempt to load a saved NetworkModel (preferred)
        # NOTE: adjust the path below to where your training pipeline actually writes the trained NetworkModel.
        network_model = None
        tried_paths = []

        # Common save locations in your training code:
        paths_to_try = [
            "final_model/network_model.pkl",      # suggested unified file (recommended)
            "final_models/network_model.pkl",     # alternative
            "artifacts/trained_model.pkl",        # common artifact path
            "artifacts/model_trainer/trained_model.pkl",
            "final_models/model.pkl",             # this contains only the raw sklearn model in your current trainer.py
        ]

        for p in paths_to_try:
            tried_paths.append(p)
            try:
                obj = load_object(p)
                # if it's a NetworkModel object, use directly
                if hasattr(obj, "predict") and hasattr(obj, "preprocessor"):
                    network_model = obj
                    break
                # If it's a raw sklearn model, we need a preprocessor too (try to load that)
                elif hasattr(obj, "predict"):
                    # try to find preprocessor
                    try:
                        preproc = load_object("final_model/preprocessor.pkl")
                        network_model = NetworkModel(preprocessor=preproc, model=obj)
                        break
                    except Exception:
                        # fallback: use model as-is (may fail if DataFrame not preprocessed)
                        network_model = NetworkModel(preprocessor=None, model=obj)
                        break
            except Exception:
                # try next path
                continue

        if network_model is None:
            # helpful debugging message rather than a cryptic failure
            raise FileNotFoundError(
                "Could not find a saved NetworkModel or sklearn model. "
                f"Tried paths: {tried_paths}. "
                "Ensure your training code saves either a NetworkModel instance (recommended) "
                "or both 'final_model/preprocessor.pkl' and 'final_models/model.pkl'."
            )

        # If preprocessor is None, the NetworkModel.predict should handle that or raise a clear error.
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        os.makedirs("prediction_data", exist_ok=True)
        df.to_csv("prediction_data/output.csv", index=False)
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        # wrap into your project's exception type for consistent handling
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
