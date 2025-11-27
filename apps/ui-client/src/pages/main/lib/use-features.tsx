import React, {
  useState,
  useCallback,
  createContext,
  useContext,
  type FC,
} from "react";
import { DashboardService } from "../api";
import { Feature } from "./types";

interface FeaturesContextType {
  features: Feature | null;
  isLoading: boolean;
  fetchFeatures: (inn: string) => Promise<void>;
}

const initialState: FeaturesContextType = {
  features: null,
  isLoading: false,
  fetchFeatures: async () => {},
};

const FeaturesContext = createContext<FeaturesContextType>(initialState);

export const FeaturesProvider: FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [features, setFeatures] = useState<Feature | null>(
    initialState.features
  );
  const [isLoading, setIsLoading] = useState(initialState.isLoading);

  const fetchFeatures = useCallback(async (inn: string) => {
    setIsLoading(true);
    const data = await DashboardService.getFeatures(inn);

    if (data) {
      setFeatures(data);
    }

    setIsLoading(false);
  }, []);

  const value = {
    features,
    isLoading,
    fetchFeatures,
  };

  return (
    <FeaturesContext.Provider value={value}>
      {children}
    </FeaturesContext.Provider>
  );
};

export const useFeatures = () => {
  return useContext(FeaturesContext);
};
