import {
  Drawer, DrawerBody, DrawerContent, DrawerHeader, DrawerOverlay,
  DrawerCloseButton, DrawerFooter, Button, useToast, VStack, Text, Box,
  Input, Alert, AlertIcon,
} from '@chakra-ui/react';
import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import { vesselCallArraySchema, type NewVesselCall } from '@/types/zodSchemas';

interface Props {
  isOpen: boolean;
  onClose(): void;
}

export default function ImportJsonDrawer({ isOpen, onClose }: Props) {
  const toast = useToast();
  const qc = useQueryClient();
  const [errorMsg, setErrorMsg] = useState('');

  const handleFile = async (file: File | null) => {
    if (!file) return;
    try {
      const text = await file.text();
      const parsed = JSON.parse(text);
      const calls = vesselCallArraySchema.parse(parsed);   // throws if invalid
      mutate(calls);                                       // trigger POSTs
    } catch (err: any) {
      setErrorMsg(err.message ?? 'Invalid JSON');
    }
  };

  const { mutate, isPending } = useMutation({
    mutationFn: async (calls: NewVesselCall[]) => {
      for (const c of calls) {
        await api.post('/vessels', c);
      }
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['vessels'] });
      toast({ status: 'success', title: 'Imported successfully' });
      onClose();
    },
    onError: () => {
      toast({ status: 'error', title: 'Import failed' });
    },
  });

  return (
    <Drawer isOpen={isOpen} placement="right" size="sm" onClose={onClose} scrollBehavior="inside">
      <DrawerOverlay />
      <DrawerContent>
        <DrawerCloseButton />
        <DrawerHeader borderBottomWidth="1px">Import JSON file</DrawerHeader>

        <DrawerBody>
          <VStack spacing={4} align="stretch">
            <Box>
              <Text fontSize="sm" mb={2}>
                Select a <b>.json</b> file that contains an <i>array</i> of vessel calls.
              </Text>
              <Input
                type="file"
                accept=".json,application/json"
                onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
              />
            </Box>

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
          <Button isLoading={isPending} colorScheme="blue" onClick={() => {}}>
            {isPending ? 'Uploading' : 'Done'}
          </Button>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}
