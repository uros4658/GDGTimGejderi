import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Tag,
  Spinner,
} from "@chakra-ui/react";
import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
  type ColumnDef,
} from "@tanstack/react-table";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import type { VesselCall } from "@/types/server";
import { predictWillChange } from "@/lib/api";

interface Props {
  data: VesselCall[];
}

export default function LiveTable({ data }: Props) {
  console.log("Vessel data1", data);
  const [sorting, setSorting] = useState<SortingState>([
    { id: "eta", desc: false },
  ]);

  const columns: ColumnDef<VesselCall>[] = [

    {
      accessorFn: (row) => row.vessel?.loa_m,
      id: "loa",
      header: "Loa (m)",
      cell: (info) => {
        const v = info.getValue<number>();
        return v != null ? v.toFixed(2) : "–";
      },
    },
    {
      accessorFn: (row) => row.vessel?.beam_m,
      id: "beam",
      header: "Beam (m)",
      cell: (info) => {
        const v = info.getValue<number>();
        return v != null ? v.toFixed(2) : "–";
      },
    },
    {
      accessorFn: (row) => row.vessel?.draft_m,
      id: "draft",
      header: "Draft (m)",
      cell: (info) => {
        const v = info.getValue<number>();
        return v != null ? v.toFixed(2) : "–";
      },
    },
    {
      accessorFn: (row) => row.vessel?.eta ?? "",
      id: "eta",
      header: "ETA",
      cell: (info) => {
        const v = info.getValue<string>();
        return v ? v.slice(0, 16).replace("T", " ") : "–";
      },
    },
 
  ];

  const defaultColumn: Partial<ColumnDef<VesselCall>> = {
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

  console.log("table rows:", table.getRowModel().rows);
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
