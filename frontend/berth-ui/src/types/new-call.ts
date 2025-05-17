import type { VesselCall } from '@/types/server';

export type NewVesselCall = Omit<VesselCall, 'id'> & {id?: string};