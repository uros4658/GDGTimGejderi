import { useQuery } from '@tanstack/react-query';
import { DateTime } from 'luxon';
import { getVessels } from '@/lib/api';
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Spinner,
  Center,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';

export default function Dashboard() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['vessels'],
    queryFn: getVessels,
  });

  if (isLoading) {
    return (
      <Center h="200px">
        <Spinner size="xl" />
      </Center>
    );
  }

  if (isError || !data) {
    return (
      <Alert status="error">
        <AlertIcon />
        API request failed. Is the backend running?
      </Alert>
    );
  }

  return (
    <Table bg="white" rounded="md" shadow="sm" overflow="hidden">
      <Thead bg="gray.100">
        <Tr>
          <Th>IMO</Th>
          <Th>Name</Th>
          <Th>Berth</Th>
          <Th>ETA (UTC)</Th>
        </Tr>
      </Thead>
      <Tbody>
        {data.map((call) => (
          <Tr key={call.id}>
            <Td>{call.vessel.imo}</Td>
            <Td>{call.vessel.name}</Td>
            <Td>{call.optimizerPlan.berthId}</Td>
            <Td>
              {DateTime.fromISO(call.vessel.eta).toFormat('dd LLL yyyy HH:mm')}
            </Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
}
