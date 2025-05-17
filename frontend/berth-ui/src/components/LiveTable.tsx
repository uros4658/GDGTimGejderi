import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Tag,
} from "@chakra-ui/react";
import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from "@tanstack/react-table";
import { useState } from "react";
import type { VesselCall } from "@/types/server";

interface Props {
  data: VesselCall[];
}

export default function LiveTable({ data }: Props) {
  const [sorting, setSorting] = useState<SortingState>([
    { id: "eta", desc: false },
  ]);

  const columns = [
    {
      accessorKey: "vessel.imo",
      header: "IMO",
      cell: (info: any) => info.getValue(),
    },
    {
      accessorKey: "vessel.name",
      header: "Name",
    },
    {
      accessorKey: "optimizerPlan.berthId",
      header: "Berth",
    },
    {
      accessorKey: "vessel.eta",
      id: "eta",
      header: "ETA",
      cell: (info: any) => info.getValue().slice(0, 16).replace("T", " "),
    },
    {
      id: "prediction",
      header: "AI",
      cell: (info: any) => {
        const row = info.row.original as VesselCall;
        const pred = row.aiPrediction?.willChange;
        return (
          <Tag colorScheme={pred ? "red" : "green"}>
            {pred ? "Change" : "Keep"}
          </Tag>
        );
      },
    },
  ];

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <TableContainer maxH="70vh" overflowY="auto">
      <Table size="sm">
        <Thead position="sticky" top={0} bg="gray.100" zIndex={1}>
          {table.getHeaderGroups().map((hg) => (
            <Tr key={hg.id}>
              {hg.headers.map((header) => (
                <Th
                  key={header.id}
                  cursor="pointer"
                  onClick={header.column.getToggleSortingHandler()}
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                  {header.column.getIsSorted() === "asc" ? " ▲" : ""}
                  {header.column.getIsSorted() === "desc" ? " ▼" : ""}
                </Th>
              ))}
            </Tr>
          ))}
        </Thead>
        <Tbody>
          {table.getRowModel().rows.map((row) => (
            <Tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <Td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </Td>
              ))}
            </Tr>
          ))}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
