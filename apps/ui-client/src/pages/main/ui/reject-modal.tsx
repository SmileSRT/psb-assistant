import type { FC } from "react";
import { Button } from "@/shared/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/shared/ui/dialog";
import { Textarea } from "@/shared/ui/textarea";

interface RejectModalProps {
  trigger: React.ReactNode;
}

export const RejectModal: FC<RejectModalProps> = ({ trigger }) => {
  return (
    <Dialog>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Оспорить прогноз</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="reason" className="text-sm font-medium">
              Причина
            </label>
            <Textarea
              id="reason"
              placeholder="Введите причину оспаривания"
              className="min-h-[100px]"
            />
          </div>
          <Button variant="brand_blue_outline" className="w-full">
            Оспорить
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
