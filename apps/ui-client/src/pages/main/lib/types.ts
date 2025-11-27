export interface FinanceDataByYear {
  СумОтч: number;
  СумПред: number;
}

export interface FinanceDataByOkved {
  2021: FinanceDataByYear;
  2022: FinanceDataByYear;
  2023: FinanceDataByYear;
  2024: FinanceDataByYear;
  2025: FinanceDataByYear;
}

export interface ShapValue {
  real_value: number;
  shap_value: number;
}

type ShapEntry = [string, ShapValue];

type ShapArray = ShapEntry[];

export interface Feature {
  "1100": FinanceDataByOkved;
  "1210": FinanceDataByOkved;
  "2100": FinanceDataByOkved;
  "2110": FinanceDataByOkved;
  "2200": FinanceDataByOkved;
  "2400": FinanceDataByOkved;
  "1360": FinanceDataByOkved;

  inn: string;
  prediction: number;
  prediction_raw: number;
  status: {
    "Действующая организация": boolean;
    "Деятельность прекращена": boolean;
    "Процесс банкротства": boolean;
    "Процесс исключения": boolean;
    "Процесс реорганизации": boolean;
    "Стадия ликвидации": boolean;
  };

  okved: number;
  positive_shap_5: ShapArray;
  negative_shap_5: ShapArray;
}

export interface IMetricaBaseInfo {
  title: string;
  value: () => string | number;
  critical: number;
  median: number;
}

export type FinanceCode =
  | "1100"
  | "1210"
  | "2100"
  | "2110"
  | "2200"
  | "2400"
  | "1360";
