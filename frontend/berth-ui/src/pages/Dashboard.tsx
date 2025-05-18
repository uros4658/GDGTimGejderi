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

  const start = startDate ? new Date(startDate) : null;
  const end = endDate ? new Date(endDate) : null;

  const filteredSchedule = useMemo(() => {
    return schedule.filter((item) => {
      const eta = new Date(item.endTime);
      if (start && eta < start) return false;
      if (end && eta > end) return false;
      return true;
    });
  }, [schedule, start, end]);

  const animationRows = useMemo(() => {
    return filteredSchedule.map((item) => ({
      id: item.vesselId,
      vessel_name: `Vessel ${item.vesselId}`,
      optimizer_berth_id: String(item.berthId),
      arrival: item.startTime,
      optimizer_start: item.startTime,
      optimizer_end: item.endTime,
    }));
  }, [filteredSchedule]);

  const avgDurationMs = useMemo(() => {
    const durations = filteredSchedule
      .filter((item) => item.actualStartTime && item.actualEndTime)
      .map(
        (item) =>
          new Date(item.actualEndTime).getTime() -
          new Date(item.actualStartTime).getTime()
      );

    if (durations.length === 0) return null;

    const total = durations.reduce((sum, d) => sum + d, 0);
    return total / durations.length;
  }, [filteredSchedule]);

  const formatDuration = (ms: number) => {
    const totalMinutes = Math.floor(ms / 60000);
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    return `${hours}h ${minutes}m`;
  };

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
          <FormLabel mb={1}>From End Time</FormLabel>
          <Input
            type="datetime-local"
            size="sm"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </FormControl>

        <FormControl maxW="250px">
          <FormLabel mb={1}>To End Time</FormLabel>
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

      {avgDurationMs !== null && (
        <Alert status="info" mb={4}>
          Average time spent in the port:{" "}
          <strong>{formatDuration(avgDurationMs)}</strong>
        </Alert>
      )}

      <LiveTable data={filteredSchedule} />

      <Drawer isOpen={isOpen} placement="right" size="xl" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Plan animation</DrawerHeader>
          <DrawerBody>
            <BoatStage calls={animationRows} playMs={120_000} />
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}
