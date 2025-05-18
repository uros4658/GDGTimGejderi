import {
  Box,
  Flex,
  HStack,
  Icon,
  Image,
  Text,
  VStack,
  useColorModeValue as mode,
} from "@chakra-ui/react";
import logo from "../assets/logo.png";
import { NavLink, Outlet } from "react-router-dom";
import { IoBoatOutline } from "react-icons/io5";
import { FiMap, FiPlusCircle, FiClock, FiActivity } from "react-icons/fi";

// 🔹 simple helper – one nav item
function NavItem({
  to,
  icon,
  children,
}: {
  to: string;
  icon: any;
  children: string;
}) {
  return (
    <HStack
      as={NavLink}
      to={to}
      px={4}
      py={3}
      rounded="md"
      _hover={{ bg: "whiteAlpha.200" }}
      _activeLink={{ bg: "whiteAlpha.300", fontWeight: "bold" }}
      w="full"
      spacing={3}
    >
      <Icon as={icon} boxSize={5} />
      <Text display={{ base: "none", lg: "inline" }}>{children}</Text>
    </HStack>
  );
}

export default function Layout() {
  return (
    <Flex minH="100vh" bg={mode("gray.50", "gray.800")}>
      {/* ░░ sidebar ░░ */}
      <Box
        as="aside"
        w={{ base: 20, lg: 260 }}
        bg="blue.700"
        color="white"
        py={8}
        px={4}
        boxShadow="xl"
      >
        <Text
          fontSize={{ base: "xl", lg: "2xl" }}
          fontWeight="bold"
          mb={10}
          textAlign={{ base: "center", lg: "left" }}
        >
          Harbor&nbsp;Pilot
        </Text>

        <VStack align="stretch" spacing={2}>
          <NavItem to="/dashboard" icon={FiMap}>
            Dashboard
          </NavItem>
          <NavItem to="/vessels" icon={IoBoatOutline}>
            Vessels
          </NavItem>
          <NavItem to="/new-call" icon={FiPlusCircle}>
            New Call
          </NavItem>
          <NavItem to="/history" icon={FiClock}>
            History
          </NavItem>
          <NavItem to="/ping" icon={FiActivity}>
            Ping
          </NavItem>
        </VStack>
      </Box>

      {/* ░░ main ░░ */}
      <Box flex="1" p={{ base: 4, lg: 8 }} overflow="auto" pos="relative">
        <Outlet />

        {/* fixed logo at bottom-left */}
        <Box pos="fixed" bottom="4" left="4" zIndex="tooltip">
          <Image
            src={logo}
            alt="Harbor Pilot Logo"
            boxSize="40px"
            objectFit="contain"
          />
        </Box>
      </Box>
    </Flex>
  );
}
