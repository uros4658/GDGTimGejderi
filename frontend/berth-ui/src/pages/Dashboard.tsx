import { useQuery } from "@tanstack/react-query";
import { Center, Spinner, Alert, AlertIcon } from "@chakra-ui/react";
import LiveTable from "@/components/LiveTable";
import { getVessels } from "@/lib/api";
import { useVesselFeed } from "@/hooks/useVesselFeed";

export default function Dashboard() {
  useVesselFeed();

  const {
    data = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["vessels"],
    queryFn: getVessels,
  });

  if (isLoading)
    return (
      <Center h="200px">
        <Spinner size="xl" />
      </Center>
    );

  if (isError)
    return (
      <Alert status="error">
        <AlertIcon />
        API request failed. Is the backend running?
      </Alert>
    );

  return <LiveTable data={data} />;
}
