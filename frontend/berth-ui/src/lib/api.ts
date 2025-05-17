import axios from "axios";
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import type { VesselCall } from "@/types/server";

const api: AxiosInstance = axios.create({
  baseURL: (import.meta.env.VITE_API_URL as string) ?? "http://localhost:8000",
});

api.interceptors.request.use((cfg: AxiosRequestConfig): AxiosRequestConfig => {
  cfg.headers ??= {};
  cfg.headers["X-API-KEY"] =
    (import.meta.env.VITE_API_KEY as string | undefined) ?? "";
  return cfg;
});

export const getVessels = async (): Promise<VesselCall[]> => {
  const resp: AxiosResponse<VesselCall[]> = await api.get("/vessels");
  return resp.data;
};

export const predictWillChange = (callId: string) =>
  api
    .post<{ willChange: boolean; confidence: number }>(`/predict`, {
      id: callId,
    })
    .then((r) => r.data);

export default api;
