// src/pages/MotionPing.tsx
import { useState } from 'react';
import { motion } from 'framer-motion';
import { Box, Button } from '@chakra-ui/react';

export default function MotionPing() {
  const [show, setShow] = useState(false);

  return (
    <Box p={8}>
      <Button onClick={() => setShow((p) => !p)}>Toggle</Button>

      {show && (
        <motion.div
          initial={{ x: -150 }}
          animate={{ x: 0 }}
          exit={{ x: 150 }}
          transition={{ duration: 0.6 }}
          style={{
            width: 120,
            height: 40,
            background: '#3182ce',
            marginTop: 24,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            borderRadius: 8,
          }}
        >
          Ping
        </motion.div>
      )}
    </Box>
  );
}
