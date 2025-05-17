import { Box, Heading } from '@chakra-ui/react';
import BoatStage from '@/components/BoatStage';

const demo = [
  {
    id: 1,
    vessel_name: 'Poseidon',
    vessel_type: 'CONTAINER',
    optimizer_berth_id: 'A1',
    optimizer_start: '2025-05-20T08:00:00Z',
    optimizer_end:   '2025-05-20T10:00:00Z',
  },
  {
    id: 2,
    vessel_name: 'Orion',
    vessel_type: 'RORO',
    optimizer_berth_id: 'B2',
    optimizer_start: '2025-05-20T08:30:00Z',
    optimizer_end:   '2025-05-20T11:00:00Z',
  },
  {
    id: 3,
    vessel_name: 'Atlas',
    vessel_type: 'BULK',
    optimizer_berth_id: 'A1',
    optimizer_start: '2025-05-20T10:30:00Z',
    optimizer_end:   '2025-05-20T12:00:00Z',
  },
  {
    id: 4,
    vessel_name: 'Hermes',
    vessel_type: 'TANKER',
    optimizer_berth_id: 'C3',
    optimizer_start: '2025-05-20T09:15:00Z',
    optimizer_end:   '2025-05-20T11:30:00Z',
  },
  {
    id: 5,
    vessel_name: 'Zephyr',
    vessel_type: 'CONTAINER',
    optimizer_berth_id: 'B2',
    optimizer_start: '2025-05-20T11:00:00Z',
    optimizer_end:   '2025-05-20T12:30:00Z',
  },
];

export default function BoatStageDemo() {
  return (
    <Box p={5}>
      <Heading size="lg" mb={5}>BoatStage demo</Heading>
      <BoatStage calls={demo} playMs={10_000}/>
    </Box>
  );
}
