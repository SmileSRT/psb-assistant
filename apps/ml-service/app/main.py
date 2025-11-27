from fastapi import FastAPI, HTTPException, UploadFile, File
from feast import FeatureStore
from app.models import CompanyFeatureRequest, CompanyFeatures
from app.file_processor import process_uploaded_files
import subprocess
from typing import List
import os
import pandas as pd
from datetime import datetime, timedelta

app = FastAPI(title="Company ML Service")

# Initialize Feature Store
def init_feast():
    """
    Initialize Feast store and ensure it's properly configured
    """
    try:
        # Check if feature store directory exists
        repo_path = "/app/feature_repo"
        if not os.path.exists(repo_path):
            raise Exception("Feature store directory not found")
        
        # Initialize store
        store = FeatureStore(repo_path=repo_path)
        
        # Apply Feast configuration
        subprocess.run(["feast", "apply"], cwd=repo_path, check=True)
        
        return store
    except Exception as e:
        print(f"Error initializing Feast: {str(e)}")
        raise

# Initialize store
store = init_feast()

def load_feast_data():
    """
    Load data into Feast store
    """
    now = datetime.now()
    five_years_ago = now - timedelta(days=5 * 365)
    try:
        # Check if data file exists
        data_path = "/app/feature_repo/data/company_data.parquet"
        if not os.path.exists(data_path):
            print(f"Data file not found at {data_path}")
            return False
        
        # Materialize features
        store.materialize(
            start_date=five_years_ago,
            end_date=datetime.now()
        )
        
        return True
    except Exception as e:
        print(f"Error loading data into Feast: {str(e)}")
        return False

# Load data on startup
load_feast_data()

@app.get("/")
async def root():
    return {"message": "Company ML Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/feast/data")
async def get_feast_data(limit: int = 100):
    """
    Get data from Feast store
    """
    try:
        # Read data directly from CSV
        data_path = "/app/feature_repo/data/resul_data.csv"
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="Data file not found")
        
        df = pd.read_csv(data_path)
        
        # Convert boolean columns to float
        bool_columns = [
            "status_Действующая организация",
            "status_Деятельность прекращена",
            "status_Процесс банкротства",
            "status_Процесс исключения",
            "status_Процесс реорганизации",
            "status_Стадия ликвидации"
        ]
        
        for col in bool_columns:
            if col in df.columns:
                df[col] = df[col].astype(float)
        
        # Convert to dict and limit rows
        data = df.head(limit).to_dict(orient="records")
        
        return {
            "status": "ok",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feast/features")
async def get_features_list():
    """
    Get list of all available features
    """
    try:
        # Read data directly from CSV
        data_path = "/app/feature_repo/data/resul_data.csv"
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="Data file not found")
        
        # Read just the header to get column names
        df = pd.read_csv(data_path, nrows=0)
        
        # Get all columns except inn, name, region, okved, and event_timestamp
        features = [col for col in df.columns if col not in ["inn", "name", "event_timestamp", "Unnamed: 0"]]
        
        # Group features by category
        feature_categories = {
            "status": [f for f in features if f.startswith("status_")],
            "financial": [f for f in features if f.startswith(("202", "Сум", "Закупки"))],
            "other": [f for f in features if f not in ["status", "financial"]]
        }
        
        return {
            "status": "ok",
            "total_features": len(features),
            "features": features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feast/status")
async def feast_status():
    """
    Check Feast store status and configuration
    """
    try:
        # Check if feature store directory exists
        repo_path = "/app/feature_repo"
        if not os.path.exists(repo_path):
            return {"status": "error", "message": "Feature store directory not found"}
        
        # Check if feature_store.yaml exists
        yaml_path = os.path.join(repo_path, "feature_store.yaml")
        if not os.path.exists(yaml_path):
            return {"status": "error", "message": "feature_store.yaml not found"}
        
        # Get list of feature views
        feature_views = store.list_feature_views()
        
        # Get list of entities
        entities = store.list_entities()
        
        # Get list of feature services
        feature_services = store.list_feature_services()
        
        return {
            "status": "ok",
            "feature_views": [fv.name for fv in feature_views],
            "entities": [e.name for e in entities],
            "feature_services": [fs.name for fs in feature_services]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/feast/entities/{entity}")
async def get_entity_info(entity: str):
    """
    Get information about a specific entity
    """
    try:
        # Get all entities
        entities = store.list_entities()
        
        # Find the requested entity
        entity_obj = next((e for e in entities if e.name == entity), None)
        if not entity_obj:
            raise HTTPException(status_code=404, detail=f"Entity {entity} not found")
        
        return {
            "name": entity_obj.name,
            "join_key": entity_obj.join_key,
            "description": entity_obj.description,
            "value_type": str(entity_obj.value_type)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload and process files
    """
    result = await process_uploaded_files(files)
    
    # After processing, update Feast data
    subprocess.run(["feast", "apply"], cwd="/app/feature_repo", check=True)
    today = datetime.now().strftime("%Y-%m-%d")
    subprocess.run(["feast", "materialize-incremental", today], cwd="/app/feature_repo", check=True)
    
    return {"message": result}

@app.post("/features", response_model=CompanyFeatures)
async def get_features(request: CompanyFeatureRequest):
    try:
        # Get features from Feast
        features = store.get_online_features(
            features=[
                "company_features:inn",
                "company_features:name",
                "company_features:region",
                "company_features:okved",
                "company_features:status_Действующая организация",
                "company_features:status_Деятельность прекращена",
                "company_features:status_Процесс банкротства",
                "company_features:status_Процесс исключения",
                "company_features:status_Процесс реорганизации",
                "company_features:status_Стадия ликвидации",
                "company_features:Закупки",
                "company_features:2020",
                "company_features:2021",
                "company_features:2022",
                "company_features:2023",
                "company_features:2024",
                "company_features:2025",
                "company_features:СумНедоим",
                "company_features:СумДолг",
                "company_features:ОстЗадолж",
            ],
            entity_rows=[{"inn": request.inn}]
        ).to_dict()

        return CompanyFeatures(
            inn=features["inn"][0],
            name=features["name"][0],
            region=features["region"][0],
            okved=features["okved"][0],
            status_active=features["status_Действующая организация"][0],
            status_terminated=features["status_Деятельность прекращена"][0],
            status_bankruptcy=features["status_Процесс банкротства"][0],
            status_exclusion=features["status_Процесс исключения"][0],
            status_reorganization=features["status_Процесс реорганизации"][0],
            status_liquidation=features["status_Стадия ликвидации"][0],
            purchases=features["Закупки"][0],
            year_2020=features["2020"][0],
            year_2021=features["2021"][0],
            year_2022=features["2022"][0],
            year_2023=features["2023"][0],
            year_2024=features["2024"][0],
            year_2025=features["2025"][0],
            sum_arrears=features["СумНедоим"][0],
            sum_debt=features["СумДолг"][0],
            remaining_debt=features["ОстЗадолж"][0]
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error retrieving features: {str(e)}")

# @app.get("/feast/features/{inn}")
# async def get_company_features(inn: str):
#     try:
#         print(f"Getting features for INN: {inn}")
#         # Get feature store
#         store = FeatureStore(repo_path="/app/feature_repo")
#         print("Feature store initialized successfully")
        
#         # Get features
#         # features = store.get_online_features(
#         #     features=["company_features:inn"],
#         #     entity_rows=[{"inn": inn}]
#         # ).to_dict()
#         features = store.get_online_features(
#             features=[
#                 "company_features:Закупки",
#                 "company_features:2020",
#                 "company_features:2021"
#             ],
#             entity_rows=[{"inn": inn}]
#         ).to_dict()
#         print(f"Features retrieved: {features}")
        
#         # Initialize result with INN
#         result = {"inn": inn}
        
#         # Add all features except 'inn' and 'event_timestamp'
#         for feature_name, values in features.items():
#             if feature_name not in ["inn", "event_timestamp"]:
#                 # If value is a list, take the first element
#                 value = values[0] if isinstance(values, list) else values
#                 result[feature_name] = value
#                 print(f"Added feature {feature_name}: {value}")
        
#         print(f"Final result: {result}")
#         return result
#     except Exception as e:
#         print(f"Error getting features: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e)) 

@app.get("/feast/features/{inn}")
async def get_company_features(inn: str):
    try:
        print(f"Getting features for INN: {inn}")

                # Загрузите данные из Parquet-файла
        df = pd.read_parquet("/app/feature_repo/data/company_data.parquet")
        
        # Инициализация Feature Store
        store = FeatureStore(repo_path="/app/feature_repo")
        
        data_path = "/app/feature_repo/data/resul_data.csv"
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="Data file not found")
        
        # Read just the header to get column names
        df = pd.read_csv(data_path, nrows=0)
        
        # Get all columns except inn, name, region, okved, and event_timestamp
        feature_list = [col for col in df.columns if col not in ["inn", "name", "event_timestamp", "Unnamed: 0"]]
        
        # Формируем список признаков для запроса
        features_to_request = [f"company_features:{feature}" for feature in feature_list]
        
        # Получение данных из Feast
        features = store.get_online_features(
            features=features_to_request,
            entity_rows=[{"inn": inn}]
        ).to_dict()
        
        # Инициализация результата
        result = {"inn": inn}
        
        # Добавление всех признаков, кроме 'inn' и 'event_timestamp'
        for feature_name, values in features.items():
            if feature_name not in ["inn", "event_timestamp"]:
                # Безопасно берем первый элемент списка, если он существует
                value = values[0] if isinstance(values, list) and len(values) > 0 else None
                result[feature_name] = value
        
        return result
    
    except Exception as e:
        print(f"Error getting features: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
