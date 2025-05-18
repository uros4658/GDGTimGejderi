// BoatStageDemo.tsx
import { Box, Heading } from '@chakra-ui/react';
import BoatStageGSAP from '@/components/BoatStage';

export const demoBig: Row[] = [
  { id: 1,  vessel_name: 'Poseidon',  optimizer_berth_id: 'A1',
    arrival: '2025-05-20T06:00:00Z',  optimizer_start: '2025-05-20T08:00:00Z',
    optimizer_end:   '2025-05-20T10:00:00Z' },

  { id: 2,  vessel_name: 'Orion',     optimizer_berth_id: 'B2',
    arrival: '2025-05-20T07:55:00Z',  optimizer_start: '2025-05-20T08:30:00Z',
    optimizer_end:   '2025-05-20T11:00:00Z' },

  { id: 3,  vessel_name: 'Atlas',     optimizer_berth_id: 'C3',
    arrival: '2025-05-20T08:10:00Z',  optimizer_start: '2025-05-20T09:00:00Z',
    optimizer_end:   '2025-05-20T11:30:00Z' },

  { id: 4,  vessel_name: 'Hermes',    optimizer_berth_id: 'A1',
    arrival: '2025-05-20T09:00:00Z',  optimizer_start: '2025-05-20T12:30:00Z',
    optimizer_end:   '2025-05-20T13:30:00Z' },

  { id: 5,  vessel_name: 'Zephyr',    optimizer_berth_id: 'B2',
    arrival: '2025-05-20T10:45:00Z',  optimizer_start: '2025-05-20T11:15:00Z',
    optimizer_end:   '2025-05-20T14:15:00Z' },

  { id: 6,  vessel_name: 'Nautilus',  optimizer_berth_id: 'D4',
    arrival: '2025-05-20T11:00:00Z',  optimizer_start: '2025-05-20T12:00:00Z',
    optimizer_end:   '2025-05-20T16:00:00Z' },

  { id: 7,  vessel_name: 'Odyssey',   optimizer_berth_id: 'C3',
    arrival: '2025-05-20T12:20:00Z',  optimizer_start: '2025-05-20T13:00:00Z',
    optimizer_end:   '2025-05-20T17:00:00Z' },

  { id: 8,  vessel_name: 'Aphrodite', optimizer_berth_id: 'E5',
    arrival: '2025-05-20T12:45:00Z',  optimizer_start: '2025-05-20T13:30:00Z',
    optimizer_end:   '2025-05-20T17:30:00Z' },

  { id: 9,  vessel_name: 'Serenity',  optimizer_berth_id: 'B2',
    arrival: '2025-05-20T13:15:00Z',  optimizer_start: '2025-05-20T14:00:00Z',
    optimizer_end:   '2025-05-20T18:00:00Z' },

  { id: 10, vessel_name: 'Europa',    optimizer_berth_id: 'A1',
    arrival: '2025-05-20T13:40:00Z',  optimizer_start: '2025-05-20T14:30:00Z',
    optimizer_end:   '2025-05-20T18:30:00Z' },

  { id: 11, vessel_name: 'Celeste',   optimizer_berth_id: 'D4',
    arrival: '2025-05-20T14:10:00Z',  optimizer_start: '2025-05-20T15:00:00Z',
    optimizer_end:   '2025-05-20T19:30:00Z' },

  { id: 12, vessel_name: 'Aurora',    optimizer_berth_id: 'F6',
    arrival: '2025-05-20T14:40:00Z',  optimizer_start: '2025-05-20T15:30:00Z',
    optimizer_end:   '2025-05-20T20:00:00Z' },

  { id: 13, vessel_name: 'Trinity',   optimizer_berth_id: 'E5',
    arrival: '2025-05-20T15:05:00Z',  optimizer_start: '2025-05-20T16:00:00Z',
    optimizer_end:   '2025-05-20T20:30:00Z' },

  { id: 14, vessel_name: 'Mirage',    optimizer_berth_id: 'C3',
    arrival: '2025-05-20T15:20:00Z',  optimizer_start: '2025-05-20T16:15:00Z',
    optimizer_end:   '2025-05-20T21:00:00Z' },

  { id: 15, vessel_name: 'Calypso',   optimizer_berth_id: 'B2',
    arrival: '2025-05-20T15:45:00Z',  optimizer_start: '2025-05-20T16:45:00Z',
    optimizer_end:   '2025-05-20T21:30:00Z' },
];
export default function BoatStageDemo() {
  return (
    <Box p={5}>
      <Heading size="lg" mb={5}>BoatStage demo</Heading>
      <BoatStageGSAP calls={demo} />
    </Box>
  );
}
