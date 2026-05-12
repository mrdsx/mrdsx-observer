import type { DailyReport } from "@/lib/schemas";
import { mapReports } from "../lib/utils";
import { ProjectReportItem } from "./ProjectReportItem";

export function DailyReports({
  dailyReports,
}: {
  dailyReports: DailyReport[];
}) {
  const sortedReports = dailyReports.sort((a, b) => {
    return new Date(a.date).getTime() - new Date(b.date).getTime();
  });
  const mappedReports = mapReports(sortedReports);

  return (
    <div className="flex flex-wrap gap-0.5">
      {mappedReports.map((report, index) => {
        return (
          <ProjectReportItem
            date={report?.date}
            worstStatus={report?.worstStatus}
            uptime={report?.uptime}
            key={report?.date ?? index}
          />
        );
      })}
    </div>
  );
}
