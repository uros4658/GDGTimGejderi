import React, { useState } from "react";
import {
  Box,
  Input,
  Select,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  HStack,
} from "@chakra-ui/react";

export type Vessel = {
  id: number;
  name: string;
  type: string;
  eta: string;
};

type Props = {
  vessels: Vessel[];
};

const VesselTable: React.FC<Props> = ({ vessels }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedType, setSelectedType] = useState("");

  const filteredVessels = vessels.filter((vessel) => {
    const matchesName = vessel.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesType = selectedType ? vessel.type === selectedType : true;
    return matchesName && matchesType;
  });

  return (
    <Box>
      <HStack mb={4} spacing={4}>
        <Input
          placeholder="Search by name"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Select
          placeholder="All Types"
          value={selectedType}
          onChange={(e) => setSelectedType(e.target.value)}
          maxW="200px"
        >
          <option value="CONTAINER">CONTAINER</option>
          <option value="RORO">RORO</option>
          <option value="BULK">BULK</option>
          <option value="TANKER">TANKER</option>
          <option value="OTHER">OTHER</option>
        </Select>
      </HStack>

      <TableContainer>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Name</Th>
              <Th>Type</Th>
              <Th>ETA</Th>
            </Tr>
          </Thead>
          <Tbody>
            {filteredVessels.map((vessel) => (
              <Tr key={vessel.id}>
                <Td>{vessel.name}</Td>
                <Td>{vessel.type}</Td>
                <Td>{new Date(vessel.eta).toLocaleString()}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default VesselTable;
