import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
} from "@chakra-ui/react";
import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type ColumnDef,
  type SortingState,
} from "@tanstack/react-table";
import { useState } from "react";
import type { PlanItem } from "@/types/server";

interface Props {
  data: PlanItem[];
}

export default function LiveTable({ data }: Props) {
  const [sorting, setSorting] = useState<SortingState>([]);

  const columns: ColumnDef<PlanItem>[] = [
    {
      accessorFn: (row) => row.startTime,
      id: "startTime",
      header: "Start Time",
      cell: (info) => {
        const v = info.getValue<string>();
        return v ? v.replace("T", " ").slice(0, 16) : "–";
      },
    },
    {
      accessorFn: (row) => row.endTime,
      id: "endTime",
      header: "End Time",
      cell: (info) => {
        const v = info.getValue<string>();
        return v ? v.replace("T", " ").slice(0, 16) : "–";
      },
    },
    {
      accessorFn: (row) => row.actualStartTime,
      id: "actualStartTime",
      header: "Actual Start",
      cell: (info) => {
        const v = info.getValue<string>();
        return v ? v.replace("T", " ").slice(0, 16) : "–";
      },
    },
    {
      accessorFn: (row) => row.actualEndTime,
      id: "actualEndTime",
      header: "Actual End",
      cell: (info) => {
        const v = info.getValue<string>();
        return v ? v.replace("T", " ").slice(0, 16) : "–";
      },
    },
    {
      accessorKey: "berthId",
      header: "Berth ID",
    },
  ];

  const defaultColumn: Partial<ColumnDef<PlanItem>> = {
    cell: (info) => {
      const v = info.getValue<any>();
      return v == null ? "–" : String(v);
    },
  };

  const table = useReactTable({
    data,
    columns,
    defaultColumn,
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
