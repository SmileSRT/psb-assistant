import pandas as pd
import re
import json
from fastapi import UploadFile, HTTPException
from typing import List
import os
from datetime import datetime

async def process_uploaded_files(files: List[UploadFile]) -> str:
    """
    Process uploaded files and transform them into Feast-compatible format
    """
    try:
        # Create temporary directory for uploaded files
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded files
        file_paths = {}
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            file_paths[file.filename] = file_path
        
        # Read all CSV files
        organizations = pd.read_csv(file_paths.get("organizations.csv"))
        contracts = pd.read_csv(file_paths.get("contracts.csv"))
        kad_arbitr = pd.read_csv(file_paths.get("kad_arbitr.csv"))
        finances = pd.read_csv(file_paths.get("finances.csv"))
        enforcements = pd.read_csv(file_paths.get("enforcements.csv"))
        egrul = pd.read_csv(file_paths.get("egrul.csv"))
        
        # Clean up data
        data = organizations.drop(columns=['Unnamed: 0.1', 'Unnamed: 0', "invalid_info", "id"])
        contracts = contracts.drop(columns=["id"])
        kad_arbitr = kad_arbitr.drop(columns=["id"])
        finances = finances.drop(columns=["id"])
        enforcements = enforcements.drop(columns=["id"])
        egrul = egrul.drop(columns=["id"])
        
        # Merge all dataframes
        data = pd.merge(data, contracts, on='inn', how='left', suffixes=('', '_1'))
        data = pd.merge(data, kad_arbitr, on='inn', how='left', suffixes=('', '_2'))
        data = pd.merge(data, finances, on='inn', how='left', suffixes=('', '_3'))
        data = pd.merge(data, enforcements, on='inn', how='left', suffixes=('', '_4'))
        data = pd.merge(data, egrul, on='inn', how='left', suffixes=('', '_5'))
        
        # Process status column
        one_hot = pd.get_dummies(data['status'], prefix='status')
        data = pd.concat([data.drop(columns=["status"]), one_hot], axis=1)
        
        # Remove fetched_at columns
        data = data.drop(columns=['fetched_at', 'fetched_at_2', "fetched_at_3", "fetched_at_4", "fetched_at_5"])
        
        # Process contracts data
        pattern = r'"Дата":\s*"(\d{4})-\d{2}-\d{2}"\s*,\s*"Цена":\s*(\d+)'
        prices = []
        dates = []
        
        for idx, row in data.iterrows():
            json_str = row['data']
            value = 0
            if pd.notna(json_str) and isinstance(json_str, str):
                matches = re.findall(pattern, json_str)
                dates.extend([match[0] for match in matches])
                price = [int(match[1]) for match in matches]
                value = sum(price)
            else:
                value = 0
            prices.append(value)
        
        data['Закупки'] = prices
        
        # Process years data
        from collections import Counter
        year_counts = Counter(dates)
        all_years = [str(year) for year in range(2020, 2026)]
        number_operation_in_data = {year: [year_counts.get(year, 0)] for year in all_years}
        year_counts_df = pd.DataFrame(number_operation_in_data)
        data = pd.concat([data, year_counts_df], axis=1)
        
        # Process enforcements data
        pattern = r'"СумНедоим":\s*"(\d+\.\d+)"'
        sum_ned = []
        
        for idx, row in data.iterrows():
            json_str = row['data_5']
            value = 0
            if pd.notna(json_str) and isinstance(json_str, str):
                matches = re.findall(pattern, json_str)
                matches = [float(now) for now in matches]
                value = sum(matches)
            else:
                value = 0
            sum_ned.append(value)
        
        data['СумНедоим'] = sum_ned
        
        # Process kad_arbitr data
        sum_dolg_list = []
        ost_zadolzh_list = []
        
        for json_str in data["data_4"]:
            try:
                if pd.notna(json_str) and isinstance(json_str, str):
                    parsed = json.loads(json_str)
                    if parsed and isinstance(parsed, list) and len(parsed) > 0:
                        sum_dolg_list.append(parsed[0].get("СумДолг", 0))
                        ost_zadolzh_list.append(parsed[0].get("ОстЗадолж", 0))
                    else:
                        sum_dolg_list.append(0)
                        ost_zadolzh_list.append(0)
                else:
                    sum_dolg_list.append(0)
                    ost_zadolzh_list.append(0)
            except (json.JSONDecodeError, KeyError, IndexError):
                sum_dolg_list.append(0)
                ost_zadolzh_list.append(0)
        
        data["СумДолг"] = sum_dolg_list
        data["ОстЗадолж"] = ost_zadolzh_list
        
        # Process finances data
        results = []
        for json_str in data["data_3"]:
            try:
                if pd.notna(json_str) and isinstance(json_str, str):
                    dat = json.loads(json_str)
                    dat = dat.get("data", {})
                    
                    years = ['2021', '2022', '2023', '2024', '2025']
                    codes = ["1100", "2110", "2200"]
                    result = {}
                    
                    for year in years:
                        if year in dat:
                            for code in codes:
                                if code in dat[year]:
                                    column_name_otch = f"{year}_{code}_СумОтч"
                                    if "СумОтч" in dat[year][code]:
                                        result[column_name_otch] = dat[year][code]["СумОтч"]
                                    else:
                                        result[column_name_otch] = 0
                                    
                                    column_name_pred = f"{year}_{code}_СумПред"
                                    if "СумПред" in dat[year][code]:
                                        result[column_name_pred] = dat[year][code]["СумПред"]
                                    else:
                                        result[column_name_pred] = 0
                                else:
                                    column_name_otch = f"{year}_{code}_СумОтч"
                                    column_name_pred = f"{year}_{code}_СумПред"
                                    result[column_name_otch] = 0
                                    result[column_name_pred] = 0
                        else:
                            for code in codes:
                                column_name_otch = f"{year}_{code}_СумОтч"
                                column_name_pred = f"{year}_{code}_СумПред"
                                result[column_name_otch] = 0
                                result[column_name_pred] = 0
                else:
                    result = {}
                    for year in ['2021', '2022', '2023', '2024', '2025']:
                        for code in ["1100", "2110", "2200"]:
                            result[f"{year}_{code}_СумОтч"] = 0
                            result[f"{year}_{code}_СумПред"] = 0
            except (json.JSONDecodeError, KeyError, IndexError):
                result = {}
                for year in ['2021', '2022', '2023', '2024', '2025']:
                    for code in ["1100", "2110", "2200"]:
                        result[f"{year}_{code}_СумОтч"] = 0
                        result[f"{year}_{code}_СумПред"] = 0
            
            results.append(result)
        
        if results:
            df_result = pd.DataFrame(results)
            df_result = df_result.fillna(0)
        else:
            df_result = pd.DataFrame()
        
        data = pd.concat([data, df_result], axis=1)
        
        # Process egrul data
        results = []
        for dats in data["data_5"]:
            reg = 0
            result = {}
            try:
                if pd.notna(dats) and isinstance(dats, str):
                    json_st = json.loads(dats)
                    if "data" in json_st:
                        dat = json_st["data"]
                        if "ДатаРег" in dat and isinstance(dat["ДатаРег"], str):
                            reg = int(dat["ДатаРег"][:4])
            except (json.JSONDecodeError, KeyError, IndexError, ValueError):
                reg = 0
            result["Дата регистрации"] = reg
            results.append(result)
        
        if results:
            df_result = pd.DataFrame(results)
            df_result = df_result.fillna(0)
        else:
            df_result = pd.DataFrame()
        
        data = pd.concat([data, df_result], axis=1)
        
        # Process kad_arbitr data for counts and sums
        results = []
        for dats, inn in zip(data["data_2"], data["inn"]):
            need_years = ['2021', '2022', '2023', '2024', '2025']
            result = {'2021':0, '2022':0, '2023':0, '2024':0, '2025':0}
            money = {'2021':0, '2022':0, '2023':0, '2024':0, '2025':0}
            try:
                if pd.notna(dats) and isinstance(dats, str):
                    json_st = json.loads(dats)
                    row = {}
                    
                    if "data" in json_st:
                        for dat in json_st["data"]:
                            for respondent in dat.get("respondents", []):
                                if str(respondent.get("inn", "")) == str(inn):
                                    year = str(dat.get("year", ""))
                                    if year in result:
                                        result[year] += 1
                                        money[year] += float(dat.get("sum", 0))
            except (json.JSONDecodeError, KeyError, IndexError, ValueError):
                pass
            
            for year in need_years:
                row[f'count_{year}'] = result[year]
                row[f'sum_{year}'] = money[year]
            results.append(row)
        
        if results:
            df_result = pd.DataFrame(results)
            df_result = df_result.fillna(0)
        else:
            df_result = pd.DataFrame()
        
        data = pd.concat([data, df_result], axis=1)
        
        # Drop JSON columns
        data = data.drop(columns=["data", 'data_2', 'data_3', 'data_4', 'data_5'])
        
        # Transform to Feast format
        df = transform_to_feast_format(data)
        
        # Save to Feast data directory
        output_path = "feature_repo/data/resul_data.csv"
        df.to_csv(output_path, index=False)
        
        # Clean up temporary files
        for file_path in file_paths.values():
            os.remove(file_path)
        os.rmdir(temp_dir)
        
        return "Files processed successfully"
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def transform_to_feast_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform processed data into Feast-compatible format
    """
    # Add event_timestamp column (required by Feast)
    df['event_timestamp'] = datetime.now()
    
    return df 