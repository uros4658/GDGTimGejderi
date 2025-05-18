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
} from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { useState, useMemo } from "react";
import LiveTable from "@/components/LiveTable";
import AnimationDrawer from "@/components/AnimationDrawer";
import { getPlan } from "@/lib/api";
import type { PlanItem } from "@/types/server";

export default function Dashboard() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const {
    data,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["plan"],
    queryFn: getPlan,
  });

  const schedule: PlanItem[] = data?.schedule ?? [];

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

        <AnimationDrawer />
      </Flex>

      <LiveTable data={schedule} />
    </>
  );
}
