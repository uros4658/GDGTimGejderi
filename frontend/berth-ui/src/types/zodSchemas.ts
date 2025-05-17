import { z } from 'zod';
export const vesselCallSchema = z.object({
  vessel: z.object({
    imo: z.number().int().min(1000000).max(9999999),
    name: z.string().min(2),
    type: z.enum(['CONTAINER', 'RORO', 'BULK', 'TANKER', 'OTHER']),
    loa_m: z.number().positive(),
    beam_m: z.number().positive(),
    draft_m: z.number().positive(),
    eta: z.string(),
  }),
  optimizerPlan: z.object({
    berthId: z.string().min(1),
    start: z.string(),
    end: z.string(),
  }),
});

export const vesselCallArraySchema = z.array(vesselCallSchema);
export type NewVesselCall = z.infer<typeof vesselCallSchema>;
