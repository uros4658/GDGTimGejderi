import { useDisclosure, Button, HStack } from '@chakra-ui/react';
import NewCallDrawer from '@/components/NewCallDrawer';
import ImportJsonDrawer from '@/components/ImportJsonDrawer';

export default function NewCall() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const imp = useDisclosure();
  return (
       <>
      <HStack spacing={4}>
        <Button colorScheme="blue" onClick={onOpen}>
          Add single vessel
        </Button>
        <Button variant="outline" onClick={imp.onOpen}>
          Import JSON
        </Button>
      </HStack>

      <NewCallDrawer isOpen={isOpen} onClose={onClose} />
      <ImportJsonDrawer isOpen={imp.isOpen} onClose={imp.onClose} />
    </>
  );
}
