import { AlertCircle, CheckCircle2, CircleX } from "lucide-react";
import type { FC } from "react";

export const StatusIcon: FC<{
  isLowTrand: boolean;
  isMiddleTrand: boolean;
  isUndefinedData: boolean;
}> = ({ isLowTrand, isMiddleTrand, isUndefinedData }) => {
  if (isLowTrand || isUndefinedData) {
    return <CircleX className="w-5 h-5 text-red-500" />;
  }

  if (isMiddleTrand && !isLowTrand) {
    return <AlertCircle className="w-5 h-5 text-orange-500" />;
  }

  return <CheckCircle2 className="w-5 h-5 text-green-500" />;
};
