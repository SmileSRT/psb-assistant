import { toast } from "sonner";

const API_BASE_URL = import.meta.env.VITE_API_HOSTNAME;

const defaultHeaders = {
  "Content-Type": "application/json",
};

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T | null> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(
        "Что-то пошло не так. Возможно, ваш ИНН некорректен или мы не знаем про данную компанию"
      );
    }

    return response.json();
  } catch (error) {
    toast.error("Ошибка запроса", {
      description:
        error instanceof Error ? error.message : "Произошла неизвестная ошибка",
    });

    return null;
  }
}

export const apiClient = {
  get: <T>(endpoint: string, options: RequestInit = {}) => {
    return request<T>(endpoint, {
      ...options,
      method: "GET",
    });
  },

  post: <T>(endpoint: string, body: string, options: RequestInit = {}) => {
    return request<T>(endpoint, {
      ...options,
      method: "POST",
      body,
    });
  },
};
