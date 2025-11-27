from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import httpx
import shap
from pydantic import BaseModel


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

# Инициализация FastAPI приложения
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загрузка модели
try:
    gbm_loaded_pickle = joblib.load('lgbm_model.pkl')  # Убедитесь, что путь корректен
except Exception as e:
    raise RuntimeError(f"Ошибка при загрузке модели: {e}")

# Определение структуры входных данных
class PredictionRequest(BaseModel):
    inn: str  # ИНН как строка

# Адрес внешнего сервиса для получения фичей
FEAST_SERVICE_URL = "http://ml-service:8000/feast/features/{inn}"

# Маршрут для выполнения предсказаний
@app.post("/predict/")
async def predict(request: PredictionRequest):
    try:
        # Получаем ИНН из запроса
        inn = request.inn

        # Отправляем GET-запрос на внешний сервис для получения фичей
        async with httpx.AsyncClient() as client:
            feast_url = FEAST_SERVICE_URL.format(inn=inn)
            response = await client.get(feast_url)

        # Проверяем статус ответа от внешнего сервиса
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Ошибка при получении фичей: {response.text}")

        # Парсим ответ от внешнего сервиса
        features = response.json()
        # Преобразуем фичи в DataFrame
        features_df = pd.DataFrame([features])
        # Приводим данные к нужным типам
        features_df = preprocess_dataframe(features_df)
        # Выполняем предсказание с использованием модели
        prediction = gbm_loaded_pickle.predict(features_df)
        # Преобразуем результат в целое число
        prediction_int = round(prediction[0])

        explainer = shap.Explainer(gbm_loaded_pickle)
        shap_values = explainer(features_df)

        shap_values_dict = {}
        for feature_name in features_df.columns:
            real_value = features_df[feature_name].values[0]
            shap_value = shap_values.values[0][features_df.columns.get_loc(feature_name)]
            shap_values_dict[feature_name] = {
                "real_value": float(real_value),
                "shap_value": float(shap_value)
            }

        top_5_positive = sorted(shap_values_dict.items(), key=lambda x: x[1]["shap_value"], reverse=True)[:5]


        # Возвращаем результаты
        result = {
            "inn": inn,
            "prediction": prediction_int,
            "prediction_raw": prediction[0],
            "status": {
                "Действующая организация": bool(features_df["status_Действующая организация"].iloc[0]),
                "Деятельность прекращена": bool(features_df["status_Деятельность прекращена"].iloc[0]),
                "Процесс банкротства": bool(features_df["status_Процесс банкротства"].iloc[0]),
                "Процесс исключения": bool(features_df["status_Процесс исключения"].iloc[0]),
                "Процесс реорганизации": bool(features_df["status_Процесс реорганизации"].iloc[0]),
                "Стадия ликвидации": bool(features_df["status_Стадия ликвидации"].iloc[0]),
            },
            "region": int(features_df["region"].iloc[0]),
            "okved": int(features_df["okved"].iloc[0]),
            "2200": {
                "2021": {
                    "СумОтч": int(features_df["2021_2200_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2021_2200_СумПред"].iloc[0]),
                },
                "2022": {
                    "СумОтч": int(features_df["2022_2200_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2022_2200_СумПред"].iloc[0]),
                },
                "2023": {
                    "СумОтч": int(features_df["2023_2200_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2023_2200_СумПред"].iloc[0]),
                },
                "2024": {
                    "СумОтч": int(features_df["2024_2200_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2024_2200_СумПред"].iloc[0]),
                },
                "2025": {
                    "СумОтч": int(features_df["2025_2200_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2025_2200_СумПред"].iloc[0]),
                },
            },
            "2100": {
                "2021": {
                    "СумОтч": int(features_df["2021_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2021_1100_СумПред"].iloc[0]),
                },
                "2022": {
                    "СумОтч": int(features_df["2022_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2022_1100_СумПред"].iloc[0]),
                },
                "2023": {
                    "СумОтч": int(features_df["2023_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2023_1100_СумПред"].iloc[0]),
                },
                "2024": {
                    "СумОтч": int(features_df["2024_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2024_1100_СумПред"].iloc[0]),
                },
                "2025": {
                    "СумОтч": int(features_df["2025_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2025_1100_СумПред"].iloc[0]),
                },
            },
            "2110": {
                "2021": {
                    "СумОтч": int(features_df["2021_2110_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2021_2110_СумПред"].iloc[0]),
                },
                "2022": {
                    "СумОтч": int(features_df["2022_2110_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2022_2110_СумПред"].iloc[0]),
                },
                "2023": {
                    "СумОтч": int(features_df["2023_2110_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2023_2110_СумПред"].iloc[0]),
                },
                "2024": {
                    "СумОтч": int(features_df["2024_2110_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2024_2110_СумПред"].iloc[0]),
                },
                "2025":{
                    "СумОтч": int(features_df["2025_2110_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2025_2110_СумПред"].iloc[0]),
                },
            },
            "1360": {
                "2021": {
                    "СумОтч": int(features_df["2021_1360_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2021_1360_СумПред"].iloc[0]),
                },
                "2022": {
                    "СумОтч": int(features_df["2022_1360_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2022_1360_СумПред"].iloc[0]),
                },
                "2023": {
                    "СумОтч": int(features_df["2023_1360_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2023_1360_СумПред"].iloc[0]),
                },
                "2024": {
                    "СумОтч": int(features_df["2024_1360_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2024_1360_СумПред"].iloc[0]),
                },
                "2025": {
                    "СумОтч": int(features_df["2025_1360_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2025_1360_СумПред"].iloc[0]),
                },
            },
            "1210": {
                "2021": {
                    "СумОтч": int(features_df["2021_1210_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2021_1210_СумПред"].iloc[0]),
                },
                "2022": {
                    "СумОтч": int(features_df["2022_1210_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2022_1210_СумПред"].iloc[0]),
                },
                "2023": {
                    "СумОтч": int(features_df["2023_1210_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2023_1210_СумПред"].iloc[0]),
                },
                "2024": {
                    "СумОтч": int(features_df["2024_1210_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2024_1210_СумПред"].iloc[0]),
                },
                "2025": {
                    "СумОтч": int(features_df["2025_1210_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2025_1210_СумПред"].iloc[0]),
                },
            },
            "1100": {
                "2021": {
                    "СумОтч": int(features_df["2021_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2021_1100_СумПред"].iloc[0]),
                },
                "2022": {
                    "СумОтч": int(features_df["2022_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2022_1100_СумПред"].iloc[0]),
                },
                "2023": {
                    "СумОтч": int(features_df["2023_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2023_1100_СумПред"].iloc[0]),
                },
                "2024": {
                    "СумОтч": int(features_df["2024_1100_СумОтч"].iloc[0]), 
                    "СумПред": int(features_df["2024_1100_СумПред"].iloc[0]),   
                },
                "2025": {
                    "СумОтч": int(features_df["2025_1100_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2025_1100_СумПред"].iloc[0]),
                },
            },
            "2400": {
                "2021": {
                    "СумОтч": int(features_df["2021_2400_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2021_2400_СумПред"].iloc[0]),
                },
                "2022": {
                    "СумОтч": int(features_df["2022_2400_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2022_2400_СумПред"].iloc[0]),
                },
                "2023": {
                    "СумОтч": int(features_df["2023_2400_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2023_2400_СумПред"].iloc[0]),   
                },
                "2024": {
                    "СумОтч": int(features_df["2024_2400_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2024_2400_СумПред"].iloc[0]),
                },
                "2025": {
                    "СумОтч": int(features_df["2025_2400_СумОтч"].iloc[0]),
                    "СумПред": int(features_df["2025_2400_СумПред"].iloc[0]),
                }
            },
            "positive_shap_5": top_5_positive,
        }
        return result
    except ValueError:
        raise HTTPException(status_code=400, detail="ИНН должен содержать только цифры.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при выполнении предсказания: {str(e)}")


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Приводит DataFrame к нужной схеме:
    - Логические значения преобразуются в числа (True -> 1, False -> 0).
    - Числовые значения приводятся к типам int64 или float64.
    - Порядок столбцов соответствует заданной схеме.
    """
    # Список всех столбцов в нужном порядке
    column_order = [
        "region", "okved", "status_Действующая организация", "status_Деятельность прекращена",
        "status_Процесс банкротства", "status_Процесс исключения", "status_Процесс реорганизации",
        "status_Стадия ликвидации", "Закупки", "2020", "2021", "2022", "2023", "2024", "2025",
        "СумНедоим", "СумДолг", "ОстЗадолж", "2021_1100_СумОтч", "2021_1100_СумПред",
        "2021_2110_СумОтч", "2021_2110_СумПред", "2021_2200_СумОтч", "2021_2200_СумПред",
        "2022_1100_СумОтч", "2022_1100_СумПред", "2022_2110_СумОтч", "2022_2110_СумПред",
        "2022_2200_СумОтч", "2022_2200_СумПред", "2023_1100_СумОтч", "2023_1100_СумПред",
        "2023_2110_СумОтч", "2023_2110_СумПред", "2023_2200_СумОтч", "2023_2200_СумПред",
        "2024_1100_СумОтч", "2024_1100_СумПред", "2024_2110_СумОтч", "2024_2110_СумПред",
        "2024_2200_СумОтч", "2024_2200_СумПред", "2025_1100_СумОтч", "2025_1100_СумПред",
        "2025_2110_СумОтч", "2025_2110_СумПред", "2025_2200_СумОтч", "2025_2200_СумПред",
        "2021_1210_СумОтч", "2021_1210_СумПред", "2021_1360_СумОтч", "2021_1360_СумПред",
        "2021_2400_СумОтч", "2021_2400_СумПред", "2022_1210_СумОтч", "2022_1210_СумПред",
        "2022_1360_СумОтч", "2022_1360_СумПред", "2022_2400_СумОтч", "2022_2400_СумПред",
        "2023_1210_СумОтч", "2023_1210_СумПред", "2023_1360_СумОтч", "2023_1360_СумПред",
        "2023_2400_СумОтч", "2023_2400_СумПред", "2024_1210_СумОтч", "2024_1210_СумПред",
        "2024_1360_СумОтч", "2024_1360_СумПред", "2024_2400_СумОтч", "2024_2400_СумПред",
        "2025_1210_СумОтч", "2025_1210_СумПред", "2025_1360_СумОтч", "2025_1360_СумПред",
        "2025_2400_СумОтч", "2025_2400_СумПред", "Дата регистрации", "count_2021", "sum_2021",
        "count_2022", "sum_2022", "count_2023", "sum_2023", "count_2024", "sum_2024",
        "count_2025", "sum_2025"
    ]

    # Преобразуем логические значения в числа
    for col in df.select_dtypes(include=['bool']).columns:
        df[col] = df[col].astype(int)

    # Приводим числовые значения к нужным типам
    for col in df.columns:
        if col in ["2020", "2021", "2022", "2023", "2024", "2025", "СумНедоим", "СумДолг", "ОстЗадолж",
                   "sum_2021", "sum_2022", "sum_2023", "sum_2024", "sum_2025"]:
            df[col] = df[col].astype(float)
        else:
            df[col] = df[col].astype(int)

    # Убеждаемся, что DataFrame содержит все столбцы в правильном порядке
    df = df.reindex(columns=column_order)

    return df