import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import type { VesselCall } from "@/types/server";

export function useVesselFeed() {
  const qc = useQueryClient();

  useEffect(() => {
    const es = new EventSource("http://localhost:8000/vessels");

    es.onmessage = (e) => {
      const update: VesselCall = JSON.parse(e.data);

      qc.setQueryData<VesselCall[]>(["vessels"], (old) => {
        if (!old) return [update];
        const idx = old.findIndex((c) => c.id === update.id);
        if (idx >= 0) {
          const copy = [...old];
          copy[idx] = update;
          return copy;
        }
        return [update, ...old];
      });
    };

    return () => es.close();
  }, [qc]);
}
