import type { Project } from "@/lib/schemas";
import { ProjectReportItem } from "./ProjectReportItem";

export function ProjectReportsView({ project }: { project: Project }) {
  const reversedDailyReports = project.dailyReports.toReversed();

  return (
    <div className="flex flex-wrap gap-0.5">
      {Array(30 - project.dailyReports.length)
        .fill(null)
        .map((_, index) => {
          // we're ok with index as key because list is static
          // biome-ignore lint/suspicious/noArrayIndexKey: .
          return <ProjectReportItem key={index} />;
        })}
      {reversedDailyReports.map((report) => {
        return (
          <ProjectReportItem
            date={report.date}
            worstStatus={report.worstStatus}
            uptime={report.uptime}
            key={report.date}
          />
        );
      })}
    </div>
  );
}
