import {
  Drawer, DrawerBody, DrawerContent, DrawerHeader, DrawerOverlay,
  DrawerCloseButton, DrawerFooter, Button, VStack, Input, Alert, AlertIcon,
  useToast,
} from '@chakra-ui/react';
import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { v4 as uuidv4 } from 'uuid';
import api from '@/lib/api';
import { vesselCallArraySchema } from '@/types/zodSchemas';
import type { NewVesselCall } from '@/types/new-call';
import type { VesselCall } from '@/types/server';

type PostPayload = NewVesselCall & { id: string };

interface Props {
  isOpen: boolean;
  onClose(): void;
}

export default function ImportJsonDrawer({ isOpen, onClose }: Props) {
  const toast = useToast();
  const qc = useQueryClient();
  const [errorMsg, setErrorMsg] = useState('');

  const { mutate, isPending } = useMutation<VesselCall[], Error, PostPayload[]>({
    mutationFn: async (payloadArr) => {
      const responses = await Promise.all(
        payloadArr.map((p) => api.post('/vessels', p).then((r) => r.data))
      );
      return responses;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['vessels'] });
      toast({ status: 'success', title: 'Imported successfully' });
      onClose();
    },
    onError: () => toast({ status: 'error', title: 'Import failed' }),
  });

  const handleFile = async (file: File | null) => {
    if (!file) return;
    try {
      const text = await file.text();
      const parsed = JSON.parse(text);
      const calls = vesselCallArraySchema.parse(parsed);
      const callsWithId: PostPayload[] = calls.map((c) => ({ id: uuidv4(), ...c }));
      mutate(callsWithId);
    } catch (err: any) {
      setErrorMsg(err.message ?? 'Invalid JSON');
    }
  };

  return (
    <Drawer isOpen={isOpen} placement="right" size="sm" onClose={onClose} scrollBehavior="inside">
      <DrawerOverlay />
      <DrawerContent>
        <DrawerCloseButton />
        <DrawerHeader borderBottomWidth="1px">Import JSON file</DrawerHeader>

        <DrawerBody>
          <VStack spacing={4} align="stretch">
            <Input
              type="file"
              accept=".json,application/json"
              onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
            />
            {errorMsg && (
              <Alert status="error">
                <AlertIcon />
                {errorMsg}
              </Alert>
            )}
          </VStack>
        </DrawerBody>

        <DrawerFooter borderTopWidth="1px">
          <Button variant="outline" mr={3} onClick={onClose}>
            Close
          </Button>
          <Button isLoading={isPending} colorScheme="blue">
            {isPending ? 'Uploading' : 'Done'}
          </Button>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}
