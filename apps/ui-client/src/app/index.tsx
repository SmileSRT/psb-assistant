import { FeaturesProvider } from "@/pages/main/lib/use-features";
import MainLayout from "./layouts/main";
import MainPage from "@/pages/main/ui";

export const App = () => {
  return (
    <FeaturesProvider>
      <MainLayout>
        <MainPage />
      </MainLayout>
    </FeaturesProvider>
  );
};

export default App;
