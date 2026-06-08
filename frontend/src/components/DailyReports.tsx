import type { DailyReport } from "@/lib/schemas";
import { mapReports } from "@/lib/utils";
import { DailyReportItem } from "./DailyReportItem";

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
    <div class="flex flex-wrap gap-0.5">
      {mappedReports.map((report) => {
        return (
          <DailyReportItem
            date={report?.date}
            worstStatus={report?.worstStatus}
            uptime={report?.uptime}
          />
        );
      })}
    </div>
  );
}
