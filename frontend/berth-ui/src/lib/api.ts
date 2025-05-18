import axios, {
  type AxiosInstance,
  type InternalAxiosRequestConfig,
  type AxiosResponse,
  AxiosHeaders,
} from "axios";
import type { VesselCall,Plan, PlanItem } from "@/types/server";

const api: AxiosInstance = axios.create({
  baseURL: (import.meta.env.VITE_API_URL as string) ?? "http://localhost:8000",
});

api.interceptors.request.use(
  (cfg: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    cfg.headers = cfg.headers ?? new AxiosHeaders();
    (cfg.headers as AxiosHeaders).set("X-API-KEY", "hackathon42");
    return cfg;
  }
);


export const getPlan = async (): Promise<Plan> => {
  const { data } = await api.get<{
    schedule: {
      vessel_id: number;
      start_time: string;
      end_time: string;
      berth_id: number;
    }[];
  }>("/plan");

  return {
    schedule: data.schedule.map((item) => ({
      vesselId: item.vessel_id,
      startTime: item.start_time,
      endTime: item.end_time,
      berthId: item.berth_id,
    })),
  };
};
export const getVessels = async (): Promise<VesselCall[]> => {
  const { data } = await api.get<any[]>("/vessels");

  return data.map((r) => ({
    id: r.id,
    vessel: {
      imo: r.imo,
      name: r.vessel_name,
      type: r.vessel_type,
      loa_m: r.loa_m,
      beam_m: r.beam_m,
      draft_m: r.draft_m,
      eta: r.eta,
      etd: r.etd,
    },
    optimizerPlan: {
      berthId: r.optimizer_berth_id,
      start: r.optimizer_start,
      end: r.optimizer_end,
    },
  }));
};

export const predictWillChange = (callId: string) =>
  api
    .post<{ willChange: boolean; confidence: number }>("/predict", {
      id: callId,
    })
    .then((r) => r.data);

export default api;
