import {
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  Button,
  Stack,
  Input,
  Select,
  FormControl,
  FormLabel,
  useToast,
} from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import type { NewVesselCall } from '@/types/new-call';

const schema = z.object({
  vessel: z.object({
    imo: z.number().int().min(1000000),
    name: z.string().min(2),
    type: z.enum(['CONTAINER', 'RORO', 'BULK', 'TANKER', 'OTHER']),
    loa_m: z.number().positive(),
    beam_m: z.number().positive(),
    draft_m: z.number().positive(),
    eta: z.string(),
  }),
  optimizerPlan: z.object({
    berthId: z.string().min(2),
    start: z.string(),
    end: z.string(),
  }),
});
type FormData = z.infer<typeof schema>;

interface Props {
  isOpen: boolean;
  onClose(): void;
}

export default function NewCallDrawer({ isOpen, onClose }: Props) {
  const toast = useToast();
  const qc = useQueryClient();

  const { register, handleSubmit, reset, formState } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      vessel: {
        type: 'CONTAINER',
      },
    },
  });


  const mut = useMutation({
    mutationFn: (payload: NewVesselCall) =>
      api.post('/vessels', payload).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({queryKey: ['vessels']});
      toast({ status: 'success', title: 'Vessel added' });
      reset();
      onClose();
    },
    onError: () => toast({ status: 'error', title: 'API error' }),
  });

  const onSubmit = (data: FormData) => {
    const payload: NewVesselCall = {
      ...data,
    };
    mut.mutate(payload);
  };

  return (
  <Drawer
    isOpen={isOpen}
    placement="right"
    size="sm"
    onClose={onClose}

  >
    <DrawerOverlay />

    <DrawerContent display="flex" overflow='scroll' flexDirection="column" h="100vh">
      <DrawerCloseButton />
      <DrawerHeader borderBottomWidth="1px">New Vessel Call</DrawerHeader>

      <form
        onSubmit={handleSubmit(onSubmit)}
        style={{ display: 'flex', flexDirection: 'column', flex: 1 }}
      >
        <DrawerBody flex="1" overflowY="auto" /* optional nicer scrollbar */ sx={{ scrollbarGutter: 'stable' }}>
          <Stack spacing={4} pb={8}>
              <FormControl isInvalid={!!formState.errors.vessel?.imo}>
                <FormLabel>IMO</FormLabel>
                <Input type="number" {...register('vessel.imo', { valueAsNumber: true })} />
              </FormControl>

              <FormControl>
                <FormLabel>Name</FormLabel>
                <Input {...register('vessel.name')} />
              </FormControl>

              <FormControl>
                <FormLabel>Type</FormLabel>
                <Select {...register('vessel.type')}>
                  <option value="CONTAINER">Container</option>
                  <option value="RORO">Ro-Ro</option>
                  <option value="BULK">Bulk</option>
                  <option value="TANKER">Tanker</option>
                  <option value="OTHER">Other</option>
                </Select>
              </FormControl>

              <FormControl>
                <FormLabel>LOA (m)</FormLabel>
                <Input type="number" step="0.1" {...register('vessel.loa_m', { valueAsNumber: true })} />
              </FormControl>

              <FormControl>
                <FormLabel>Beam (m)</FormLabel>
                <Input type="number" step="0.1" {...register('vessel.beam_m', { valueAsNumber: true })} />
              </FormControl>

              <FormControl>
                <FormLabel>Draft (m)</FormLabel>
                <Input type="number" step="0.1" {...register('vessel.draft_m', { valueAsNumber: true })} />
              </FormControl>

              <FormControl>
                <FormLabel>ETA</FormLabel>
                <Input type="datetime-local" {...register('vessel.eta')} />
              </FormControl>


              <FormControl>
                <FormLabel>Berth ID</FormLabel>
                <Input {...register('optimizerPlan.berthId')} />
              </FormControl>

              <FormControl>
                <FormLabel>Window start</FormLabel>
                <Input type="datetime-local" {...register('optimizerPlan.start')} />
              </FormControl>

              <FormControl>
                <FormLabel>Window end</FormLabel>
                <Input type="datetime-local" {...register('optimizerPlan.end')} />
              </FormControl>
            </Stack>
          </DrawerBody>

          <DrawerFooter borderTopWidth="1px">
            <Button variant="outline" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button
              colorScheme="blue"
              type="submit"
              isLoading={mut.isPending}
            >
              Save
            </Button>
          </DrawerFooter>
        </form>
      </DrawerContent>
    </Drawer>
  );
}
