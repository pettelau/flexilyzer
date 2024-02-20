"use client";
import {
  ReportTeamResponse,
  ValueTypesOutput,
} from "@/extensions/data-contracts";
import { AnalyzerWithOutputs, TeamReports } from "@/types/analyzerDefinitions";
import {
  Table,
  TableHeader,
  TableBody,
  TableColumn,
  TableRow,
  TableCell,
  Chip,
  Progress,
  Tooltip,
  Dropdown,
  Checkbox,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  Button,
  Selection,
  DropdownSection,
  SortDescriptor,
  Select,
  SelectItem,
} from "@nextui-org/react";
import { Key, useMemo, useState } from "react";

interface OverviewTableParams {
  analyzersWithOutputs: AnalyzerWithOutputs[];
  allReports: TeamReports;
}

type FlatMappedOutputs = {
  analyzerId: number;
  key_name: string;
  value_type: ValueTypesOutput;
  display_name?: string | null | undefined;
  extended_metadata?: null | undefined;
  id: number;
};

export default function OverviewTable({
  allReports,
  analyzersWithOutputs,
}: OverviewTableParams) {
  const [visibleColumns, setVisibleColumns] = useState(
    new Set(
      analyzersWithOutputs.flatMap((analyzer) =>
        analyzer.outputs.map((output) => output.id.toString())
      )
    )
  );

  const [sortDescriptor, setSortDescriptor] = useState<SortDescriptor>();
  const [selectedKeys, setSelectedKeys] = useState<Selection>(new Set([]));

  const [selectedOutputFilterIds, setSelectedOutputFilterIds] =
    useState<Selection>(new Set([]));

  const allReportsList: ReportTeamResponse[][] = Object.values(allReports).map(
    (r) => r.reports
  );

  const sortedItems = useMemo(() => {
    if (sortDescriptor == undefined) return allReportsList;

    const col = sortDescriptor.column as string;
    const [descriptor, id] = col.split("-");

    if ("Team" === descriptor)
      return sortDescriptor.direction == "ascending"
        ? allReportsList.reverse()
        : allReportsList;

    return [...allReportsList].sort((a, b) => {
      const firstReport = a.find((report) =>
        report.report.hasOwnProperty(descriptor)
      );
      const secondReport = b.find((report) =>
        report.report.hasOwnProperty(descriptor)
      );

      let firstValue = firstReport ? firstReport.report[descriptor] : null;
      let secondValue = secondReport ? secondReport.report[descriptor] : null;

      if (typeof firstValue === "string") {
        firstValue = parseFloat(firstValue);
      }
      if (typeof secondValue === "string") {
        secondValue = parseFloat(secondValue);
      }

      if (firstValue == null) return 1;
      if (secondValue == null) return -1;

      // Comparison
      let comparison = 0;
      if (firstValue < secondValue) {
        comparison = -1;
      } else if (firstValue > secondValue) {
        comparison = 1;
      }

      // Handle sorting direction
      return sortDescriptor.direction === "descending"
        ? -comparison
        : comparison;
    });
  }, [sortDescriptor, allReportsList]);

  // console.log(allReportsList);

  const toggleColumnVisibility = (columnId: Key) => {
    setVisibleColumns((prevState) => {
      const newState = new Set(prevState);
      const columnIdStr = columnId.toString();
      if (newState.has(columnIdStr)) {
        newState.delete(columnIdStr);
      } else {
        newState.add(columnIdStr);
      }
      return newState;
    });
  };

  const initalColumn: FlatMappedOutputs[] = [
    {
      analyzerId: 0,
      key_name: "Team",
      display_name: "Team",
      value_type: ValueTypesOutput.Int,
      id: 0,
    },
  ];

  const flatMappedOutputs = analyzersWithOutputs.flatMap((analyzer) =>
    analyzer.outputs
      .filter((output) => visibleColumns.has(output.id.toString()))
      .map((output) => ({
        ...output,
        analyzerId: analyzer.id,
      }))
  );

  const allColumnOutputs = initalColumn.concat(flatMappedOutputs);

  // const handleFilterChange = (outputId: string) => {
  //   if (outputId === "") {
  //     setSelectedOutputFilterIds(undefined);
  //   } else {
  //     setSelectedOutputFilterIds((prev) => {
  //       if (prev === undefined) {
  //         return [Number(outputId)];
  //       } else {
  //         return [...prev, Number(outputId)];
  //       }
  //     });
  //   }
  // };

  const renderFilterParameters = () => {
    console.log(selectedOutputFilterIds);
    return "Hello";
    // if (selectedOutputFilterIds !== undefined) {
    //   const selectedOutput = flatMappedOutputs.find(
    //     (output) => output.id === selectedOutputFilterId
    //   );

    //   switch (selectedOutput?.value_type) {
    //     case ValueTypesOutput.Bool:
    //       return "hello";
    //   }
    // }
  };

  const topContent = (
    <div className="flex flex-col justify-center">
      <div className="flex flex-row justify-center">
        <Dropdown>
          <DropdownTrigger>
            <Button size="md" variant="solid" className="w-[130px]">
              Select Columns
            </Button>
          </DropdownTrigger>
          <DropdownMenu
            closeOnSelect={false}
            aria-label="Choose Columns"
            onAction={toggleColumnVisibility}
          >
            {analyzersWithOutputs.map((analyzer) => (
              <DropdownSection key={analyzer.id} title={analyzer.analyzer_name}>
                {analyzer.outputs.map((output) => (
                  <DropdownItem
                    key={output.id}
                    textValue={output.id.toString()}
                  >
                    <Checkbox
                      isSelected={visibleColumns.has(output.id.toString())}
                    >
                      {output.display_name
                        ? output.display_name
                        : output.key_name}
                    </Checkbox>
                  </DropdownItem>
                ))}
              </DropdownSection>
            ))}
          </DropdownMenu>
        </Dropdown>
      </div>
      <div className="flex flex-col justify-center">
        <Select
          className="max-w-xs"
          selectionMode="multiple"
          label="Select columns to filter on"
          selectedKeys={selectedOutputFilterIds}
          onSelectionChange={setSelectedOutputFilterIds}
        >
          {flatMappedOutputs
            .filter((output) =>
              [
                ValueTypesOutput.Int,
                ValueTypesOutput.Range,
                ValueTypesOutput.Bool,
              ].includes(output.value_type)
            )
            .map((output) => (
              <SelectItem key={output.id} value={output.id}>
                {output.display_name ? output.display_name : output.key_name}
              </SelectItem>
            ))}
        </Select>
        <div>{renderFilterParameters()}</div>
      </div>
      <div>
        <span className="text-default-400 text-small">
          Total {allReportsList.length} teams
        </span>
      </div>
    </div>
  );

  const getValue = (item: ReportTeamResponse[], columnKey: string) => {
    const [name, id] = columnKey.split("-");

    if (name === "Team") return item[0].team_id;
    const report = item.find(
      (r: ReportTeamResponse) => r.analyzer_id === Number(id)
    );
    const value = report ? report.report[name] : undefined;

    const output = flatMappedOutputs.find(
      (output) => output.analyzerId === Number(id) && output.key_name === name
    );
    if (!output) return value;

    switch (output.value_type) {
      case ValueTypesOutput.Range:
        interface RangeMetadata {
          fromRange: number;
          toRange: number;
        }

        const extendedMetadata =
          output.extended_metadata as unknown as RangeMetadata;

        return (
          value && (
            <Tooltip
              delay={0}
              closeDelay={0}
              content={
                <>
                  {value} / {extendedMetadata.toRange}
                </>
              }
            >
              <Progress
                aria-label={output.key_name}
                size="md"
                value={value}
                minValue={extendedMetadata.fromRange}
                maxValue={extendedMetadata.toRange}
                color={
                  value / extendedMetadata.toRange > 0.65
                    ? "success"
                    : "warning"
                }
                className="max-w-md"
              />
            </Tooltip>
          )
        );
      case ValueTypesOutput.Str:
        return value;
      case ValueTypesOutput.Bool:
        return (
          value !== undefined && (
            <Chip
              size="sm"
              variant="solid"
              color={(value as boolean) ? "success" : "danger"}
              className="text-white"
            >
              {value ? "Yes" : "No"}
            </Chip>
          )
        );
      case ValueTypesOutput.Int:
        return value;
      default:
        return "N/A";
    }
  };

  return (
    <>
      <Table
        topContent={topContent}
        onSortChange={setSortDescriptor}
        sortDescriptor={sortDescriptor}
        selectedKeys={selectedKeys}
        selectionMode="multiple"
        onSelectionChange={setSelectedKeys}
        isHeaderSticky
      >
        <TableHeader columns={allColumnOutputs}>
          {(column) => {
            const name = column.display_name
              ? column.display_name
              : column.key_name;
            return (
              <TableColumn
                key={`${column.key_name}-${column.analyzerId}`}
                allowsSorting
              >
                {name}
              </TableColumn>
            );
          }}
        </TableHeader>
        <TableBody items={sortedItems}>
          {(item: ReportTeamResponse[]) => (
            <TableRow key={item[0].team_id}>
              {(columnKey) => (
                <TableCell>{getValue(item, columnKey as string)}</TableCell>
              )}
            </TableRow>
          )}
        </TableBody>
        {/* <TableBody emptyContent={"No rows to display."}>{[]}</TableBody> */}
      </Table>
    </>
  );
}