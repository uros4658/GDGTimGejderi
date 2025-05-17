// import {
//   Table,
//   Thead,
//   Tbody,
//   Tr,
//   Th,
//   Td,
//   TableContainer,
//   Tag,
//   Spinner,
// } from "@chakra-ui/react";
// import {
//   flexRender,
//   getCoreRowModel,
//   getSortedRowModel,
//   useReactTable,
//   type SortingState,
// } from "@tanstack/react-table";
// import { useQuery } from "@tanstack/react-query";
// import { useState } from "react";
// import type { VesselCall } from "@/types/server";
// import { predictWillChange } from "@/lib/api";

// interface Props {
//   data: VesselCall[];
// }

// export default function LiveTable({ data }: Props) {
//   const [sorting, setSorting] = useState<SortingState>([
//     { id: "eta", desc: false },
//   ]);

//   const columns = [
//     {
//       accessorKey: "vessel.imo",
//       header: "IMO",
//       cell: (info: any) => info.getValue(),
//     },
//     {
//       accessorKey: "vessel.name",
//       header: "Name",
//     },
//     {
//       accessorKey: "optimizerPlan.berthId",
//       header: "Berth",
//     },
//     {
//       accessorKey: "vessel.eta",
//       id: "eta",
//       header: "ETA",
//       cell: (info: any) => info.getValue().slice(0, 16).replace("T", " "),
//     },
//     {
//       id: "prediction",
//       header: "AI",
//       cell: (info: any) => {
//         const row = info.row.original as VesselCall;

//         // first, use any server-side prediction if it’s already there
//         const serverPred = row.aiPrediction?.willChange;
//         const serverConf = row.aiPrediction?.confidence;

//         // frontend cache key => ['predict', row.id]
//         const { data } = useQuery({
//           queryKey: ["predict", row.id],
//           queryFn: () => predictWillChange(row.id),
//           enabled: serverPred === undefined,
//           staleTime: 5 * 60 * 1000,
//         });

//         const willChange =
//           serverPred !== undefined ? serverPred : data?.willChange;
//         const conf = serverConf !== undefined ? serverConf : data?.confidence;

//         if (willChange === undefined) return <Spinner size="xs" />;

//         return (
//           <Tag
//             colorScheme={willChange ? "red" : "green"}
//             title={conf ? `Conf: ${(conf * 100).toFixed(1)} %` : undefined}
//           >
//             {willChange ? "Change" : "Keep"}
//           </Tag>
//         );
//       },
//     },
//   ];

//   const table = useReactTable({
//     data,
//     columns,
//     state: { sorting },
//     onSortingChange: setSorting,
//     getCoreRowModel: getCoreRowModel(),
//     getSortedRowModel: getSortedRowModel(),
//   });

//   return (
//     <TableContainer maxH="70vh" overflowY="auto">
//       <Table size="sm">
//         <Thead position="sticky" top={0} bg="gray.100" zIndex={1}>
//           {table.getHeaderGroups().map((hg) => (
//             <Tr key={hg.id}>
//               {hg.headers.map((header) => (
//                 <Th
//                   key={header.id}
//                   cursor="pointer"
//                   onClick={header.column.getToggleSortingHandler()}
//                 >
//                   {flexRender(
//                     header.column.columnDef.header,
//                     header.getContext()
//                   )}
//                   {header.column.getIsSorted() === "asc" ? " ▲" : ""}
//                   {header.column.getIsSorted() === "desc" ? " ▼" : ""}
//                 </Th>
//               ))}
//             </Tr>
//           ))}
//         </Thead>
//         <Tbody>
//           {table.getRowModel().rows.map((row) => (
//             <Tr key={row.id}>
//               {row.getVisibleCells().map((cell) => (
//                 <Td key={cell.id}>
//                   {flexRender(cell.column.columnDef.cell, cell.getContext())}
//                 </Td>
//               ))}
//             </Tr>
//           ))}
//         </Tbody>
//       </Table>
//     </TableContainer>
//   );
// }
