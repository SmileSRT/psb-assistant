from datetime import datetime, timedelta
from feast import Entity, Feature, FeatureService, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String, Bool
from feast.data_format import FileFormat
import pandas as pd
from feast.data_source import DataSource
from feast.infra.offline_stores.file_source import FileSource

# Define the entity
company = Entity(
    name="company",
    join_keys=["inn"],
    description="Company identifier"
)

# Define the data source
company_source = FileSource(
    path="/app/feature_repo/data/company_data.parquet",
    timestamp_field="event_timestamp"
)

# Define feature view
company_features = FeatureView(
    name="company_features",
    entities=[company],
    ttl=timedelta(days=365),
    schema=[
        Field(name="inn", dtype=Int64),
        Field(name="name", dtype=String),
        Field(name="region", dtype=Int64),
        Field(name="okved", dtype=Int64),
        Field(name="status_Действующая организация", dtype=Bool),
        Field(name="status_Деятельность прекращена", dtype=Bool),
        Field(name="status_Процесс банкротства", dtype=Bool),
        Field(name="status_Процесс исключения", dtype=Bool),
        Field(name="status_Процесс реорганизации", dtype=Bool),
        Field(name="status_Стадия ликвидации", dtype=Bool),
        Field(name="Закупки", dtype=Int64),
        Field(name="2020", dtype=Float32),
        Field(name="2021", dtype=Float32),
        Field(name="2022", dtype=Float32),
        Field(name="2023", dtype=Float32),
        Field(name="2024", dtype=Float32),
        Field(name="2025", dtype=Float32),
        Field(name="СумНедоим", dtype=Float32),
        Field(name="СумДолг", dtype=Float32),
        Field(name="ОстЗадолж", dtype=Float32),
        Field(name="2021_1100_СумОтч", dtype=Int64),
        Field(name="2021_1100_СумПред", dtype=Int64),
        Field(name="2021_2110_СумОтч", dtype=Int64),
        Field(name="2021_2110_СумПред", dtype=Int64),
        Field(name="2021_2200_СумОтч", dtype=Int64),
        Field(name="2021_2200_СумПред", dtype=Int64),
        Field(name="2022_1100_СумОтч", dtype=Int64),
        Field(name="2022_1100_СумПред", dtype=Int64),
        Field(name="2022_2110_СумОтч", dtype=Int64),
        Field(name="2022_2110_СумПред", dtype=Int64),
        Field(name="2022_2200_СумОтч", dtype=Int64),
        Field(name="2022_2200_СумПред", dtype=Int64),
        Field(name="2023_1100_СумОтч", dtype=Int64),
        Field(name="2023_1100_СумПред", dtype=Int64),
        Field(name="2023_2110_СумОтч", dtype=Int64),
        Field(name="2023_2110_СумПред", dtype=Int64),
        Field(name="2023_2200_СумОтч", dtype=Int64),
        Field(name="2023_2200_СумПред", dtype=Int64),
        Field(name="2024_1100_СумОтч", dtype=Int64),
        Field(name="2024_1100_СумПред", dtype=Int64),
        Field(name="2024_2110_СумОтч", dtype=Int64),
        Field(name="2024_2110_СумПред", dtype=Int64),
        Field(name="2024_2200_СумОтч", dtype=Int64),
        Field(name="2024_2200_СумПред", dtype=Int64),
        Field(name="2025_1100_СумОтч", dtype=Int64),
        Field(name="2025_1100_СумПред", dtype=Int64),
        Field(name="2025_2110_СумОтч", dtype=Int64),
        Field(name="2025_2110_СумПред", dtype=Int64),
        Field(name="2025_2200_СумОтч", dtype=Int64),
        Field(name="2025_2200_СумПред", dtype=Int64),
        Field(name="2021_1210_СумОтч", dtype=Int64),
        Field(name="2021_1210_СумПред", dtype=Int64),
        Field(name="2021_1360_СумОтч", dtype=Int64),
        Field(name="2021_1360_СумПред", dtype=Int64),
        Field(name="2021_2400_СумОтч", dtype=Int64),
        Field(name="2021_2400_СумПред", dtype=Int64),
        Field(name="2022_1210_СумОтч", dtype=Int64),
        Field(name="2022_1210_СумПред", dtype=Int64),
        Field(name="2022_1360_СумОтч", dtype=Int64),
        Field(name="2022_1360_СумПред", dtype=Int64),
        Field(name="2022_2400_СумОтч", dtype=Int64),
        Field(name="2022_2400_СумПред", dtype=Int64),
        Field(name="2023_1210_СумОтч", dtype=Int64),
        Field(name="2023_1210_СумПред", dtype=Int64),
        Field(name="2023_1360_СумОтч", dtype=Int64),
        Field(name="2023_1360_СумПред", dtype=Int64),
        Field(name="2023_2400_СумОтч", dtype=Int64),
        Field(name="2023_2400_СумПред", dtype=Int64),
        Field(name="2024_1210_СумОтч", dtype=Int64),
        Field(name="2024_1210_СумПред", dtype=Int64),
        Field(name="2024_1360_СумОтч", dtype=Int64),
        Field(name="2024_1360_СумПред", dtype=Int64),
        Field(name="2024_2400_СумОтч", dtype=Int64),
        Field(name="2024_2400_СумПред", dtype=Int64),
        Field(name="2025_1210_СумОтч", dtype=Int64),
        Field(name="2025_1210_СумПред", dtype=Int64),
        Field(name="2025_1360_СумОтч", dtype=Int64),
        Field(name="2025_1360_СумПред", dtype=Int64),
        Field(name="2025_2400_СумОтч", dtype=Int64),
        Field(name="2025_2400_СумПред", dtype=Int64),
        Field(name="Дата регистрации", dtype=Int64),
        Field(name="count_2021", dtype=Int64),
        Field(name="sum_2021", dtype=Float32),
        Field(name="count_2022", dtype=Int64),
        Field(name="sum_2022", dtype=Float32),
        Field(name="count_2023", dtype=Int64),
        Field(name="sum_2023", dtype=Float32),
        Field(name="count_2024", dtype=Int64),
        Field(name="sum_2024", dtype=Float32),
        Field(name="count_2025", dtype=Int64),
        Field(name="sum_2025", dtype=Float32),
    ],
    source=company_source,
)

# Define feature service
company_service = FeatureService(
    name="company_service",
    features=[company_features]
) 