import { useEffect } from 'react';
import { motion, useAnimationControls } from 'framer-motion';
import { Box, Text } from '@chakra-ui/react';

type RawCall = {
  id: string;
  vessel?: { name?: string };
  optimizerPlan?: { berthId?: string; start?: string; end?: string };
  vessel_name?: string;
  optimizer_berth_id?: string;
  optimizer_start?: string;
  optimizer_end?: string;
  berthId?: string;
  eta?: string;
  etd?: string;
};

interface Props {
  calls: RawCall[];
  speed?: number; 
}

function toFinal(c: RawCall) {
  return {
    id: c.id,
    name:
      c.vessel?.name ??
      c.vessel_name ??
      'Unknown',
    berthId:
      c.berthId ??
      c.optimizerPlan?.berthId ??
      c.optimizer_berth_id ??
      '???',
    eta:
      c.eta ??
      c.optimizerPlan?.start ??
      c.optimizer_start ??
      new Date().toISOString(),
    etd:
      c.etd ??
      c.optimizerPlan?.end ??
      c.optimizer_end ??
      new Date().toISOString(),
  };
}

export default function BoatStage({ calls, speed = 1 }: Props) {
  const ctrl = useAnimationControls();

  const timeline = calls
    .map(toFinal)
    .filter((r) => r.berthId && r.eta && r.etd)
    .sort(
      (a, b) => new Date(a.eta).getTime() - new Date(b.eta).getTime()
    );

  const t0 = timeline.length ? new Date(timeline[0].eta).getTime() : 0;
  const hourMs = 3600000 / speed;

  useEffect(() => {
  timeline.forEach((c) => {
    const eta = new Date(c.eta).getTime();
    const etd = new Date(c.etd).getTime();

    const hoursToMs = (h: number) => h * 1000;
    const delay = hoursToMs((eta - t0) / hourMs);
    const stay  = hoursToMs((etd - eta) / hourMs);

    setTimeout(() => {
      ctrl.start(i =>
  i === c.id ? { x: '-110vw', transition: { duration: 1 } } : {}
);

      setTimeout(() => {
       ctrl.start(i =>
  i === c.id ? { x: '-110vw', transition: { duration: 1 } } : {}
);
      }, stay);
    }, delay);
  });
}, [timeline, ctrl, t0, hourMs]);

  const berthOrder = [...new Set(timeline.map((c) => c.berthId))].sort().reverse();
  const laneY = (berth: string) => `${25 * berthOrder.indexOf(berth)}%`;

  return (
    <Box pos="relative" w="100%" h="300px" bg="blue.50" overflow="hidden">
      {timeline.map((c) => (
        <motion.div
          key={c.id}
          custom={c.id}
          animate={ctrl}
          initial={{ x: '110vw', y: laneY(c.berthId) }}
          style={{
            position: 'absolute',
            width: 80,
            height: 24,
            background: '#0364e6',
            borderRadius: 4,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontSize: 10,
          }}
        >
          <Text>{c.name}</Text>
        </motion.div>
      ))}
    </Box>
  );
}
