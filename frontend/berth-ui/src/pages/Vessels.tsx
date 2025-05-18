// pages/Vessels.tsx
import React, { useEffect, useState } from "react";
import {
  Box,
  Heading,
  Spinner,
  Center,
  ChakraProvider,
} from "@chakra-ui/react";
import Vessel from "../components/VesselsTable";
import VesselTable from "../components/VesselsTable";

type Vessel = {
  id: number;
  name: string;
  type: string;
  eta: string;
};

const Vessels: React.FC = () => {
  const [vessels, setVessels] = useState<Vessel[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVessels = async () => {
      try {
        const response = await fetch("http://localhost:8000/vessels");
        const data = await response.json();
        setVessels(data);
      } catch (error) {
        console.error("Failed to fetch vessels:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchVessels();
  }, []);

  return (
    <ChakraProvider>
      <Box p={6}>
        <Heading mb={4}>Vessels</Heading>
        {loading ? (
          <Center>
            <Spinner size="xl" />
          </Center>
        ) : (
          <VesselTable vessels={vessels} />
        )}
      </Box>
    </ChakraProvider>
  );
};

export default Vessels;
