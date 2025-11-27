import type { FC, PropsWithChildren } from "react";
import { AppSidebar } from "@/shared/ui/app-sidebar";
import { SidebarProvider, SidebarTrigger } from "@/shared/ui/sidebar";
import { Toaster } from "sonner";

const MainLayout: FC<PropsWithChildren> = ({ children }) => (
  <SidebarProvider>
    <AppSidebar />

    <div className="w-full">
      <header className="w-full h-[50px] border-b border-b-sidebar-border flex justify-between md:pr-5 p-2">
        <div className="flex items-center gap-1">
          <img src="/icons/logo-psb.png" alt="PSB Logo" className="h-8" />
          <SidebarTrigger />
        </div>
      </header>

      <main>{children}</main>
    </div>
    <Toaster />
  </SidebarProvider>
);

export default MainLayout;
