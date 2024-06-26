import {
  ReportTeamResponse,
  ValueTypesOutput,
} from "@/extensions/data-contracts";
import { FilterState, FlatMappedOutputs } from "@/types/tableDefinitions";
import { SortDescriptor } from "@nextui-org/react";

const filterReports = (
  allReportsList: ReportTeamResponse[][],
  filterState: FilterState,
  allFlatMappedOutputs: FlatMappedOutputs[],
) => {
  return allReportsList.filter((teamReports) => {
    return teamReports.every((report) => {
      let passesFilters = true;

      for (const [key, filter] of Object.entries(filterState)) {
        const output = allFlatMappedOutputs.find(
          (output) => output.id === Number(key),
        );
        if (output === undefined) {
          continue;
        }

        let reportValue = report.report[output.key_name];

        if (typeof reportValue === "object") {
          reportValue = reportValue["value"];
        }

        if (reportValue === undefined) {
          continue;
        }

        switch (filter.value_type) {
          case ValueTypesOutput.Bool:
            if (
              filter.boolValue !== undefined &&
              reportValue !== filter.boolValue
            ) {
              passesFilters = false;
            }
            break;
          case ValueTypesOutput.Int:
          case ValueTypesOutput.Range:
            if (filter.intValue) {
              const { min, max } = filter.intValue;
              if (min !== undefined && (reportValue as number) < min) {
                passesFilters = false;
              }
              if (max !== undefined && (reportValue as number) > max) {
                passesFilters = false;
              }
            }
            break;
        }
      }

      return passesFilters;
    });
  });
};

const sortReports = (
  sortDescriptor: SortDescriptor | undefined,
  filteredReports: ReportTeamResponse[][],
) => {
  if (sortDescriptor == undefined) return filteredReports;

  const col = sortDescriptor.column as string;
  const [descriptor] = col.split("-");

  if ("Team" === descriptor)
    return sortDescriptor.direction == "ascending"
      ? filteredReports.slice().reverse()
      : filteredReports;

  return [...filteredReports].sort((a, b) => {
    const firstReport = a.find((report) =>
      report.report.hasOwnProperty(descriptor),
    );
    const secondReport = b.find((report) =>
      report.report.hasOwnProperty(descriptor),
    );

    let firstValue = firstReport ? firstReport.report[descriptor] : null;
    let secondValue = secondReport ? secondReport.report[descriptor] : null;

    if (typeof firstValue === "object") {
      firstValue = firstValue["value"];
    }

    if (typeof secondValue === "object") {
      secondValue = secondValue["value"];
    }

    if (typeof firstValue === "string") {
      firstValue = parseFloat(firstValue);
    }
    if (typeof secondValue === "string") {
      secondValue = parseFloat(secondValue);
    }

    // when some teams dont have values for report outputs
    if (sortDescriptor.direction === "descending") {
      if (firstValue == null) return 1;
      if (secondValue == null) return -1;
    } else {
      if (firstValue == null) return -1;
      if (secondValue == null) return 1;
    }

    let comparison = 0;
    if (firstValue < secondValue) {
      comparison = -1;
    } else if (firstValue > secondValue) {
      comparison = 1;
    }

    return sortDescriptor.direction === "descending" ? -comparison : comparison;
  });
};

export { filterReports, sortReports };
