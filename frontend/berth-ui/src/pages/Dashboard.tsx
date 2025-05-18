import {
  Center,
  Spinner,
  Alert,
  AlertIcon,
  Flex,
  Spacer,
  Heading,
  Input,
  FormControl,
  FormLabel,
  Button,
  useDisclosure,
  Drawer,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  DrawerHeader,
  DrawerBody,
} from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { useState, useMemo } from "react";
import LiveTable from "@/components/LiveTable";
import BoatStage from "@/components/BoatStage";
import { getPlan } from "@/lib/api";
import type { PlanItem } from "@/types/server";

export default function Dashboard() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const { data, isLoading, isError } = useQuery({
    queryKey: ["plan"],
    queryFn: getPlan,
  });

  const schedule: PlanItem[] = data?.schedule ?? [];

  const { isOpen, onOpen, onClose } = useDisclosure();

  const animationRows = useMemo(() => {
    return schedule.map((item) => ({
      id: item.vesselId,
      vessel_name: `Vessel ${item.vesselId}`,
      optimizer_berth_id: String(item.berthId),
      arrival: item.actualArrivalTime,
      optimizer_start: item.startTime,
      optimizer_end: item.endTime,
    }));
  }, [schedule]);

  if (isLoading) {
    return (
      <Center h="200px">
        <Spinner size="xl" />
      </Center>
    );
  }
  if (isError) {
    return (
      <Alert status="error">
        <AlertIcon />
        API request failed. Is the backend running?
      </Alert>
    );
  }

  return (
    <>
      <Flex align="center" mb={4} gap={4} wrap="wrap">
        <Heading size="md">Live Berth Plan</Heading>
        <Spacer />

        <FormControl maxW="250px">
          <FormLabel mb={1}>From ETA</FormLabel>
          <Input
            type="datetime-local"
            size="sm"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </FormControl>

        <FormControl maxW="250px">
          <FormLabel mb={1}>To ETA</FormLabel>
          <Input
            type="datetime-local"
            size="sm"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </FormControl>

        <Button colorScheme="purple" onClick={onOpen}>
          Play animation
        </Button>
      </Flex>

      <LiveTable data={schedule} />

      <Drawer isOpen={isOpen} placement="right" size="xl" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Plan animation</DrawerHeader>
          <DrawerBody>
            <BoatStage calls={animationRows} playMs={1_000_000} />
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}
