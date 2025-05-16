import { Flex, Box, Link, VStack } from '@chakra-ui/react';
import { NavLink, Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <Flex minH="100vh">
      {/* ----- Sidebar ------------------------------------------------ */ }
      <Box
        as="aside"
        w="220px"
        bg="blue.600"
        color="white"
        p={6}
        fontWeight="medium"
      >
        <Box fontSize="2xl" fontWeight="bold" mb={8}>
          Berth UI
        </Box>

        <VStack align="start" spacing={4}>
          <Link as={NavLink} to="/dashboard" _activeLink={{ fontWeight: 'bold' }}>
            Dashboard
          </Link>
          <Link as={NavLink} to="/new-call" _activeLink={{ fontWeight: 'bold' }}>
            New Call
          </Link>
          <Link as={NavLink} to="/history" _activeLink={{ fontWeight: 'bold' }}>
            History
          </Link>
        </VStack>
      </Box>

      {/* ----- Main outlet -------------------------------------------- */ }
      <Box flex="1" p={6} bg="gray.50">
        <Outlet />
      </Box>
    </Flex>
  );
}
