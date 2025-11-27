import { useState, type FC } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/shared/ui/card";
import { ChartContainer } from "@/shared/ui/chart";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/shared/ui/select";
import { financialCodes, transformData } from "../lib/utils";
import { FinanceCode, FinanceDataByOkved } from "../lib/types";

const chartConfig = {
  value: {
    label: "Активы",
    color: "#ea5616",
  },
};

const financeCodes = ["1100", "1210", "2100", "2110", "2200", "2400", "1360"];

export const StatsChart: FC<{
  features: Record<FinanceCode, FinanceDataByOkved>;
}> = ({ features }) => {
  const [currentCode, setCurrentCode] = useState<FinanceCode>("2400");

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex justify-between items-center">
          {financialCodes[currentCode].name}
          <Select
            onValueChange={(value) => setCurrentCode(value as FinanceCode)}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Выберите показатель" />
            </SelectTrigger>
            <SelectContent>
              {financeCodes.map((code) => (
                <SelectItem value={code} key={code}>
                  {financialCodes[code].name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardTitle>
        <CardDescription>
          За последние 5 лет{" "}
          <span className="text-[10px] font-bold text-gray-700">
            (тыс. руб)
          </span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <ResponsiveContainer width="100%" height="100%" minHeight={300}>
            <LineChart data={transformData(features[currentCode])}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#ea5616"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  );
};
