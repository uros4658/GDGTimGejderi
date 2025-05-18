import {
  Alert,
  AlertIcon,
  Button,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  Input,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FiCheckCircle, FiXCircle } from "react-icons/fi";

import api from "@/lib/api";

interface Props {
  isOpen: boolean;
  onClose(): void;
  api_url: string;
}

export default function ImportJsonDrawer({ isOpen, onClose, api_url }: Props) {
  const toast = useToast();
  const qc = useQueryClient();
  const [errorMsg, setErrorMsg] = useState("");

  const importMut = useMutation<any[], Error, any[]>({
    mutationFn: async (payloadArr) =>
      Promise.all(
        payloadArr.map((p) => api.patch(api_url, p).then((r) => r.data))
      ),
    onSuccess: () => {
      qc.invalidateQueries();
      toast({
        status: "success",
        title: "Imported successfully",
        icon: <FiCheckCircle />,
      });
      onClose();
    },
    onError: () =>
      toast({
        status: "error",
        title: "Import failed",
        icon: <FiXCircle />,
      }),
  });

  const handleFile = async (file: File | null) => {
    if (!file) return;
    try {
      const text = await file.text();
      const parsed = JSON.parse(text);

      const payload: any[] = Array.isArray(parsed) ? parsed : [parsed];

      importMut.mutate(payload);
      setErrorMsg("");
    } catch (err: any) {
      setErrorMsg(err.message ?? "Invalid JSON");
    }
  };

  return (
    <Drawer
      isOpen={isOpen}
      placement="right"
      size="sm"
      onClose={onClose}
      scrollBehavior="inside"
    >
      <DrawerOverlay />
      <DrawerContent>
        <DrawerCloseButton />

        <DrawerHeader borderBottomWidth="1px">Import JSON</DrawerHeader>

        <DrawerBody>
          <VStack spacing={6} align="stretch">
            <VStack spacing={1} align="stretch">
              <Text fontWeight="medium">Choose a .json file</Text>
              <Input
                type="file"
                accept=".json,application/json"
                onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
              />
            </VStack>

            {errorMsg && (
              <Alert status="error">
                <AlertIcon />
                {errorMsg}
              </Alert>
            )}
          </VStack>
        </DrawerBody>

        <DrawerFooter borderTopWidth="1px">
          <Button variant="ghost" mr={3} onClick={onClose}>
            Cancel
          </Button>
          <Button
            colorScheme="blue"
            isLoading={importMut.isPending}
            loadingText="Uploading"
            onClick={onClose}
          >
            Done
          </Button>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}
