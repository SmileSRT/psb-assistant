import { apiClient } from "@/shared/api/api-client";
import { Feature } from "../lib/types";

export class DashboardService {
  static async getFeatures(inn: string) {
    const response = await apiClient.post<Feature>(
      `/predict/`,

      JSON.stringify({ inn })
    );

    return response;
  }
}
