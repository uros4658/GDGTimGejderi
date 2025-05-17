import { Button, Card, CardBody, Heading, HStack } from '@chakra-ui/react';
import { useDisclosure } from '@chakra-ui/react';
import { FiPlus, FiUpload } from 'react-icons/fi';

import NewCallDrawer from '@/components/NewCallDrawer';
import ImportJsonDrawer from '@/components/ImportJsonDrawer';

export default function NewCall() {
  const single = useDisclosure();
  const bulk = useDisclosure();

  return (
    <>
      <Card shadow="lg">
        <CardBody>
          <Heading size="md" mb={6}>
            Create / Import Vessel Calls
          </Heading>

          <HStack spacing={4}>
            <Button
              leftIcon={<FiPlus />}
              colorScheme="blue"
              onClick={single.onOpen}
            >
              Add single vessel
            </Button>

            <Button
              leftIcon={<FiUpload />}
              variant="outline"
              onClick={bulk.onOpen}
            >
              Import JSON
            </Button>
          </HStack>
        </CardBody>
      </Card>

      <NewCallDrawer isOpen={single.isOpen} onClose={single.onClose} />
      <ImportJsonDrawer isOpen={bulk.isOpen} onClose={bulk.onClose} />
    </>
  );
}
