import { useEffect } from 'react';
import { motion, useAnimationControls } from 'framer-motion';
import { Box, Text } from '@chakra-ui/react';

export type FinalCall = {
  id: string;
  vessel: { name: string };
  berthId: string;
  eta: string;   
  etd: string;   
};

interface Props {
  calls: FinalCall[];
  speed?: number;    
}

export default function BoatStage({ calls, speed = 2 }: Props) {
  const ctrl = useAnimationControls();
  const timeline = [...calls].sort(
    (a, b) => new Date(a.eta).getTime() - new Date(b.eta).getTime()
  );
  const t0 = timeline.length ? new Date(timeline[0].eta).getTime() : 0;
  const hourMs = 3600000 / speed;

  useEffect(() => {
    timeline.forEach((c) => {
      const eta = new Date(c.eta).getTime();
      const etd = new Date(c.etd).getTime();
      const delay  = ((eta - t0) / hourMs);
      const stay   = ((etd - eta) / hourMs);

      setTimeout(() => {
        ctrl.start(i => i === c.id ? { x: '0%', transition: { duration: 1 } } : {});
        setTimeout(() => {
          ctrl.start(i => i === c.id ? { x: '-110%', transition: { duration: 1 } } : {});
        }, stay);
      }, delay);
    });
  }, [timeline, ctrl, t0, hourMs]);

  const berthOrder = [...new Set(timeline.map(c => c.berthId))].sort().reverse();
  const laneY = (berth: string) => `${25 * berthOrder.indexOf(berth)}%`;

  return (
    <Box pos="relative" w="100%" h="300px" bg="blue.50" overflow="hidden">
      {timeline.map(c => (
        <motion.div
          key={c.id}
          custom={c.id}
          animate={ctrl}
          initial={{ x: '110%', y: laneY(c.berthId) }}
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
          <Text>{c.vessel.name}</Text>
        </motion.div>
      ))}
    </Box>
  );
}
