import { FinanceDataByOkved, ShapValue } from "./types";

export const YEARS = [2025, 2024, 2023, 2022, 2021] as const;

export function transformData(source: FinanceDataByOkved) {
  const result = [];

  for (const [year, values] of Object.entries(source)) {
    const date = `${year}.01.01`;
    result.push({ date, value: values.СумОтч / 1000 });
  }

  return result;
}

interface FinancialCodesDictionary {
  [code: string]: {
    name: string;
    description: string;
    formula?: string;
    unit?: string;
  };
}

export const getMetric = (
  dividendFeatures?: FinanceDataByOkved,
  delimeterFeatures?: FinanceDataByOkved,
  isPercent: boolean = false
) => {
  for (const year of YEARS) {
    const dividend = Number(dividendFeatures?.[year]?.СумОтч);
    const delimeter = Number(delimeterFeatures?.[year]?.СумОтч);

    if (!dividend || !delimeter) {
      if (year === 2021) {
        return { value: "Н/Д", currentYear: 2021 };
      }

      continue;
    }

    return {
      value: ((dividend / delimeter) * (isPercent ? 100 : 1)).toFixed(2),
      currentYear: year,
    };
  }
};

export function transformShapeData(data: (string | ShapValue)[][]) {
  return data.map((item) => ({
    name: item[0],
    shap_value:
      typeof item[1] === "object"
        ? parseFloat(item[1].shap_value.toFixed(5))
        : item[0],
    real_value:
      typeof item[1] === "object"
        ? parseFloat(item[1].real_value.toFixed(5))
        : item[0],
  }));
}

export const formattedToPercent = (value: number) => {
  const result = value * 100;

  return `${Math.round(result)}% `;
};

export const financialCodes: FinancialCodesDictionary = {
  "1100": {
    name: "Внеоборотные активы (1100)",
    description:
      "Суммарная стоимость внеоборотных активов компании (основные средства, нематериальные активы, долгосрочные вложения)",
  },
  "1210": {
    name: "Запасы (1210)",
    description:
      "Сырьё, материалы, готовая продукция, товары для перепродажи и другие материально-производственные запасы",
  },
  "2100": {
    name: "Валовая прибыль (убыток) (2100)",
    description:
      "Прибыль от основной деятельности до вычета управленческих и коммерческих расходов",
  },
  "2110": {
    name: "Выручка (2110)",
    description:
      "Доходы от обычных видов деятельности (продажа товаров, услуг)",
  },
  "2200": {
    name: "Прибыль (убыток) от продаж (2200)",
    description:
      "Финансовый результат от основной деятельности после вычета всех расходов",
    formula:
      "2100 (Валовая прибыль) - 2210 (Коммерческие расходы) - 2220 (Управленческие расходы)",
    unit: "руб.",
  },
  "2400": {
    name: "Чистая прибыль (убыток) (2400)",
    description:
      "Конечный финансовый результат после всех налогов и дополнительных расходов",
    formula:
      "2300 (Прибыль до налогообложения) - 2410 (Налог на прибыль) ± прочие налоговые корректировки",
    unit: "руб.",
  },
  "1360": {
    name: "Резервный капитал (1360)",
    description:
      "Часть собственного капитала, предназначенная для покрытия убытков и погашения облигаций",
    unit: "руб.",
  },
};
