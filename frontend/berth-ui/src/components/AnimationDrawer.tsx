import {
  Drawer, DrawerOverlay, DrawerContent, DrawerCloseButton,
  DrawerHeader, DrawerBody, IconButton, useDisclosure,
} from '@chakra-ui/react';
import { Play } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import BoatStage, { FinalCall } from '@/components/BoatStage';

export default function AnimationDrawer() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { data } = useQuery({
    queryKey: ['vessels'],
    queryFn: () => api.get<FinalCall[]>('/vessels').then(r => r.data),
    staleTime: 0,
  });

  return (
    <>
      <IconButton aria-label="Play animation" icon={<Play />} onClick={onOpen} />
      <Drawer isOpen={isOpen} onClose={onClose} size="full">
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Berth Animation</DrawerHeader>
          <DrawerBody p={0}>
            {data && <BoatStage calls={data} speed={2} />}
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}
