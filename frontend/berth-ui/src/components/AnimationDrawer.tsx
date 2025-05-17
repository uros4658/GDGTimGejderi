import {
  Drawer, DrawerOverlay, DrawerContent, DrawerCloseButton,
  DrawerHeader, DrawerBody, IconButton, useDisclosure,
} from '@chakra-ui/react';
import { FiPlay } from 'react-icons/fi';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import BoatStage from '@/components/BoatStage';

export default function AnimationDrawer() {
  const d = useDisclosure();
  const { data = [] } = useQuery({
    queryKey: ['vessels'],
    queryFn: () => api.get('/vessels').then(r => r.data),
    staleTime: 0,
  });

  return (
    <>
      <IconButton aria-label="Play animation" icon={<FiPlay />} onClick={d.onOpen} />
      <Drawer isOpen={d.isOpen} onClose={d.onClose} size="full">
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Berth Animation</DrawerHeader>
          <DrawerBody p={0}>
             <BoatStage calls={data} playMs={20_000}/>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}
