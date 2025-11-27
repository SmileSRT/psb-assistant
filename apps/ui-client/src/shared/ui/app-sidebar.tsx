import { useState, type FC } from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "../ui/sidebar";
import { FileUpload } from "./file-upload";
import { Input } from "./input";
import { useFeatures } from "@/pages/main/lib/use-features";
import LoadingButton from "./loading-button";

export const AppSidebar: FC = () => {
  const [inn, setInn] = useState<string>("");
  const { fetchFeatures, isLoading } = useFeatures();

  return (
    <Sidebar>
      <SidebarHeader>
        <h5 className="text-blue-750 text-2xl font-bold">
          ПСБ{" "}
          <span className="text-orange-350 text-sm font-normal">{`<Ассистент>`}</span>
        </h5>
      </SidebarHeader>

      <SidebarContent className="p-4">
        <SidebarGroup>
          <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-col gap-4">
            <Input
              placeholder="ИНН Компании"
              value={inn}
              onChange={(event) => setInn(event.target.value)}
            />
            <FileUpload />
            <LoadingButton
              variant="brand_orange"
              size="sm"
              onClick={() => fetchFeatures(inn)}
              isLoading={isLoading}
            >
              Прогноз
            </LoadingButton>
          </div>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
};
