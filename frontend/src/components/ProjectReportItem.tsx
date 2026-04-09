import { Popover } from "antd";
import { cn, mapDate } from "@/lib/utils";
import { useThemeStore } from "@/stores/themeStore";

type ReportItemProps = {
  date?: string;
  worstStatus?: string;
  uptime?: number;
};

export function ProjectReportItem({
  date,
  worstStatus,
  uptime,
}: ReportItemProps) {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  return (
    <Popover
      title={date !== undefined && mapDate(date)}
      content={
        <div>
          <p className="flex justify-between gap-2">
            Worst status: <span>{worstStatus ?? "—"}</span>
          </p>
          <p className="flex justify-between gap-4">
            Uptime: <span>{uptime !== undefined ? `${uptime}%` : "—"}</span>
          </p>
        </div>
      }
    >
      <div className="w-2 h-6 relative group">
        <div
          className={cn(
            "w-2 h-6 rounded absolute group-hover:bottom-1 bottom-0 duration-50",
            worstStatus === undefined && "bg-gray-300",
            worstStatus === undefined && isDarkMode && "bg-gray-500",
            worstStatus === "outage"
              ? "bg-red-500"
              : worstStatus === "degraded"
                ? "bg-yellow-500"
                : worstStatus === "operational" && "bg-green-500",
          )}
        />
      </div>
    </Popover>
  );
}
