import axios, {
  type AxiosInstance,
  type InternalAxiosRequestConfig,
  type AxiosResponse,
  AxiosHeaders,
} from 'axios';
import type { VesselCall } from '@/types/server';


const api: AxiosInstance = axios.create({
  baseURL: (import.meta.env.VITE_API_URL as string) ?? 'http://localhost:8000',
});


api.interceptors.request.use(
  (cfg: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    cfg.headers = cfg.headers ?? new AxiosHeaders();
    (cfg.headers as AxiosHeaders).set(
      'X-API-KEY',
      (import.meta.env.VITE_API_KEY as string | undefined) ?? ''
    );
    return cfg;
  },
);

export const getVessels = async (): Promise<VesselCall[]> => {
  const resp: AxiosResponse<VesselCall[]> = await api.get('/vessels');
  return resp.data;
};

export const predictWillChange = (callId: string) =>
  api
    .post<{ willChange: boolean; confidence: number }>('/predict', { id: callId })
    .then((r) => r.data);

export default api;
