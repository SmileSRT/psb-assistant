import { useMemo, type FC } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import { Button } from "@/shared/ui/button";
import { cn } from "@/shared/lib/utils";
import { CircleCheck, CircleX, Loader2 } from "lucide-react";
import { StatsChart } from "./stats-chart";
import { RejectModal } from "./reject-modal";
import { useFeatures } from "../lib/use-features";
import {
  formattedToPercent,
  getMetric,
  transformShapeData,
} from "../lib/utils";

import { StatusIcon } from "./status-icon";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/shared/ui/table";

export const Dashboard: FC = () => {
  const { features, isLoading } = useFeatures();

  const statusList = Object.entries(features?.status || {}).map(
    ([title, value]) => {
      return {
        title,
        value,
      };
    }
  );

  const shapeData = transformShapeData(features?.positive_shap_5 || []);

  const metrics = useMemo(
    () => [
      {
        title: "Рентабельность продаж",
        critical: 0,
        median: 3,
        ...getMetric(features?.[2400], features?.[2110], true),
      },
      {
        title: "Оборачиваемость запасов",
        critical: 2,
        median: 4,
        ...getMetric(features?.[2110], features?.[1100], false),
      },
      {
        title: "Убыточность продаж",
        critical: 10,
        median: 5,
        ...getMetric(features?.[2200], features?.[2110], true),
      },
    ],
    [features]
  );

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-[calc(100vh-100px)]">
        <Loader2 className="w-10 h-10 animate-spin text-orange-350" />
      </div>
    );
  }

  if (features) {
    return (
      <div className="flex flex-col gap-4 p-4 max-w-[1400px] mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          <Card className="lg:col-span-1 gap-2 max-h-[200px] overflow-y-auto">
            <CardHeader>
              <CardTitle>О компании</CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-gray-600">
              <ul>
                <li className="flex gap-2 ">
                  <h5 className="font-bold">ИНН</h5>
                  <span className="text-gray-500">{features.inn}</span>
                </li>
                <li className="flex gap-2">
                  <h5 className="font-bold">ОКВЭД</h5>
                  <span className="text-gray-500">{features.okved}</span>
                </li>
                <li className="mt-2">
                  <h5 className="text-sm font-bold text-blue-750">Статусы</h5>
                  <ul>
                    {statusList.map(({ title, value }) => {
                      return (
                        <li
                          key={title}
                          className="flex items-center gap-2 mt-1"
                        >
                          <h5 className="font-bold">{title}:</h5>
                          <span
                            className={cn("text-red-400 font-extrabold", {
                              "text-green-500": value,
                            })}
                          >
                            {value ? (
                              <CircleCheck width={20} />
                            ) : (
                              <CircleX width={20} />
                            )}
                          </span>
                        </li>
                      );
                    })}
                  </ul>
                </li>
              </ul>
            </CardContent>
          </Card>

          {metrics.map((metric, index) => {
            const isLowTrend = Number(metric.value) < metric.critical;
            const isMiddleTrend = Number(metric.value) < metric.median;
            const isUndefinedData = metric.value === "Н/Д";

            return (
              <Card
                key={index}
                className={cn(
                  "text-center bg-gray-50 border-2 border-green-300",
                  {
                    "border-red-400 bg-red-50": isLowTrend || isUndefinedData,
                  },
                  {
                    "border-orange-400 bg-orange-100/50":
                      isMiddleTrend && !isLowTrend,
                  }
                )}
              >
                <CardHeader className="p-2">
                  <div className="flex flex-col lg:flex-row items-center justify-center gap-2">
                    <CardTitle className="text-2xl font-bold">
                      {metric.value}
                    </CardTitle>
                    <StatusIcon
                      isLowTrand={isLowTrend}
                      isMiddleTrand={isMiddleTrend}
                      isUndefinedData={isUndefinedData}
                    />
                  </div>
                </CardHeader>
                <CardContent className="p-2 text-gray-500">
                  <h5 className="font-bold text-blue-750">{metric.title}</h5>
                  <span className="text-xs">За {metric?.currentYear}г.</span>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Card className="w-full gap-2">
            <CardHeader>
              <CardTitle>Финансовая устойчивость</CardTitle>
            </CardHeader>
            <CardContent className="overflow-y-auto flex flex-col gap-2 justify-between h-full text-sm">
              <div
                className={cn(
                  "text-center p-2 border rounded-lg font-bold",
                  features.prediction
                    ? "bg-red-50 border-red-400"
                    : "bg-green-50 border-green-400"
                )}
              >
                <h5 className="flex text-blue-750 items-center justify-center gap-2">
                  Вероятность квази-дефолта:{" "}
                  <span
                    className={cn("bg-green-400 p-1 rounded-lg text-white", {
                      "bg-red-400": features.prediction,
                    })}
                  >
                    {formattedToPercent(features.prediction_raw)}
                  </span>
                </h5>
              </div>

              <div>
                <Table>
                  <TableCaption>Влияние параметров модели</TableCaption>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Параметр</TableHead>
                      <TableHead>Реальные значения</TableHead>
                      <TableHead>Степень влияния</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {shapeData &&
                      shapeData.map((item) => {
                        const isObject = typeof item === "object";
                        const key = isObject ? item.name : item;

                        return (
                          <TableRow key={key.toString()}>
                            <TableCell className="font-medium">
                              {isObject ? item.name.toString() : "Н/Д"}
                            </TableCell>
                            <TableCell>
                              {isObject ? item.real_value.toString() : "Н/Д"}
                            </TableCell>
                            <TableCell>
                              {isObject ? item.shap_value.toString() : "Н/Д"}
                            </TableCell>
                          </TableRow>
                        );
                      })}
                  </TableBody>
                </Table>
              </div>

              <div className="flex justify-center gap-2 w-full mt-4">
                <Button variant="brand_orange">Подтвердить</Button>
                <RejectModal
                  trigger={
                    <Button variant="brand_blue_outline">Оспорить</Button>
                  }
                />
              </div>
            </CardContent>
          </Card>

          <StatsChart features={features} />
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-center items-center h-[calc(100vh-100px)]">
      <p className="text-gray-500 w-[300px] text-center">
        Для <span className="text-orange-350 font-bold">прогноза</span> и
        подсчета метрик необходимо ввести{" "}
        <span className="text-orange-350 font-bold">ИНН</span> компании
      </p>
    </div>
  );
};
