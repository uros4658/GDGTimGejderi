// BoatStageDemo.tsx
import { Box, Heading } from '@chakra-ui/react';
import BoatStageGSAP from '@/components/BoatStage';

export const demo: Row[] = [
  {
    id: 1,
    vessel_name: 'Poseidon',
    optimizer_berth_id: 'A1',
    arrival:        '2025-05-20T06:00:00Z',          // anchorage
    optimizer_start:'2025-05-20T08:00:00Z',          // dock
    optimizer_end:  '2025-05-20T10:00:00Z',          // leave
  },
  {
    id: 2,
    vessel_name: 'Orion',
    optimizer_berth_id: 'B2',
    arrival:        '2025-05-20T07:55:00Z',
    optimizer_start:'2025-05-20T08:30:00Z',
    optimizer_end:  '2025-05-20T11:00:00Z',
  },
  {
    id: 3,
    vessel_name: 'Atlas',
    optimizer_berth_id: 'C3',
    arrival:        '2025-05-20T08:10:00Z',
    optimizer_start:'2025-05-20T09:00:00Z',
    optimizer_end:  '2025-05-20T11:30:00Z',
  },
  {
    id: 4,
    vessel_name: 'Hermes',
    optimizer_berth_id: 'A1',
    arrival:        '2025-05-20T09:00:00Z',
    optimizer_start:'2025-05-20T12:30:00Z',
    optimizer_end:  '2025-05-20T13:30:00Z',
  },
  {
    id: 5,
    vessel_name: 'Zephyr',
    optimizer_berth_id: 'B2',
    arrival:        '2025-05-20T10:45:00Z',
    optimizer_start:'2025-05-20T11:15:00Z',
    optimizer_end:  '2025-05-20T14:15:00Z',
  },
  {
    id: 6,
    vessel_name: 'Nautilus',
    optimizer_berth_id: 'D4',
    arrival:        '2025-05-20T11:00:00Z',
    optimizer_start:'2025-05-20T12:00:00Z',
    optimizer_end:  '2025-05-20T16:00:00Z',
  },
  {
    id: 7,
    vessel_name: 'Odyssey',
    optimizer_berth_id: 'C3',
    arrival:        '2025-05-20T12:20:00Z',
    optimizer_start:'2025-05-20T13:00:00Z',
    optimizer_end:  '2025-05-20T17:00:00Z',
  },
];
export default function BoatStageDemo() {
  return (
    <Box p={5}>
      <Heading size="lg" mb={5}>BoatStage demo</Heading>
      <BoatStageGSAP calls={demo} />
    </Box>
  );
}
