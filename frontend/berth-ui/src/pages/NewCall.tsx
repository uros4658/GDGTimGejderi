import { useState } from "react";
import {
  Button,
  Card,
  CardBody,
  Heading,
  HStack,
  NumberInput,
  NumberInputField,
} from "@chakra-ui/react";
import { useDisclosure } from "@chakra-ui/react";
import { FiPlus, FiUpload } from "react-icons/fi";

import NewCallDrawer from "@/components/NewCallDrawer";
import ImportJsonDrawer from "@/components/ImportJsonDrawer";

export default function NewCall() {
  const single = useDisclosure();
  const bulk = useDisclosure();

  const [currentApiUrl, setCurrentApiUrl] = useState<string>("");
  const [humanPlanActualId, setHumanPlanActualId] = useState<number | null>(
    null
  );
  const [actualPlanActualId, setActualPlanActualId] = useState<number | null>(
    null
  );

  return (
    <>
      <Card shadow="lg" mb={6}>
        <CardBody>
          <Heading size="md" mb={6}>
            Import Human Plan
          </Heading>

          <HStack spacing={4}>
            <Button
              leftIcon={<FiUpload />}
              variant="outline"
              onClick={() => {
                setCurrentApiUrl("/plan/human-fix");
                bulk.onOpen();
              }}
            >
              Import JSON
            </Button>
          </HStack>
        </CardBody>
      </Card>

      <Card shadow="lg" mb={6}>
        <CardBody>
          <Heading size="md" mb={6}>
            Import Actual Plan
          </Heading>

          <HStack spacing={4}>
            <Button
              leftIcon={<FiUpload />}
              variant="outline"
              onClick={() => {
                setCurrentApiUrl("/vessels/1000/actual-plan");
                bulk.onOpen();
              }}
            >
              Import JSON
            </Button>
          </HStack>
        </CardBody>
      </Card>

      <Card shadow="lg" mb={6}>
        <CardBody>
          <Heading size="md" mb={6}>
            Edit Past Human Plan
          </Heading>

          <HStack spacing={4}>
            <NumberInput
              value={humanPlanActualId ?? ""}
              onChange={(_, valueAsNumber) =>
                setHumanPlanActualId(valueAsNumber)
              }
              min={1}
              max={999999}
            >
              <NumberInputField placeholder="Actual ID" />
            </NumberInput>

            <Button
              leftIcon={<FiUpload />}
              variant="outline"
              isDisabled={!humanPlanActualId}
              onClick={() => {
                if (humanPlanActualId) {
                  setCurrentApiUrl(`/plan/${humanPlanActualId}/human-fix`);
                  bulk.onOpen();
                }
              }}
            >
              Import JSON
            </Button>
          </HStack>
        </CardBody>
      </Card>

      <Card shadow="lg" mb={6}>
        <CardBody>
          <Heading size="md" mb={6}>
            Edit Past Actual Plan
          </Heading>

          <HStack spacing={4}>
            <NumberInput
              value={actualPlanActualId ?? ""}
              onChange={(_, valueAsNumber) =>
                setActualPlanActualId(valueAsNumber)
              }
              min={1}
              max={999999}
            >
              <NumberInputField placeholder="Actual ID" />
            </NumberInput>

            <Button
              leftIcon={<FiUpload />}
              variant="outline"
              isDisabled={!actualPlanActualId}
              onClick={() => {
                if (actualPlanActualId) {
                  setCurrentApiUrl(
                    `/vessels/${actualPlanActualId}/actual-plan`
                  );
                  bulk.onOpen();
                }
              }}
            >
              Import JSON
            </Button>
          </HStack>
        </CardBody>
      </Card>

      <NewCallDrawer isOpen={single.isOpen} onClose={single.onClose} />
      <ImportJsonDrawer
        isOpen={bulk.isOpen}
        onClose={bulk.onClose}
        api_url={currentApiUrl}
      />
    </>
  );
}
