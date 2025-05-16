// Auto-generated — do not edit

export interface VesselCall {
  /**
   * UUID v4
   */
  id: string;
  vessel: {
    imo: number;
    name: string;
    type: "CONTAINER" | "RORO" | "BULK" | "TANKER" | "OTHER";
    loa_m: number;
    beam_m: number;
    draft_m: number;
    eta: string;
  };
  optimizerPlan: BerthPlan;
  aiPrediction?: {
    modelVersion: string;
    willChange: boolean;
    confidence?: number;
    suggestedPlan?: BerthPlan;
  };
  humanPlan?: BerthPlan;
  actualExecution?: {
    berthId: string;
    ata: string;
    atd: string;
  };
}
export interface BerthPlan {
  berthId: string;
  start: string;
  end: string;
}
