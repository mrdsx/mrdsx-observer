import { Popover } from "antd";
import { cn } from "@/lib/utils";
import { useThemeStore } from "@/stores/themeStore";

const ITEM_CLASS_NAME = "w-2 h-6 rounded";

type ReportItemProps = {
  date?: string;
  worstStatus?: string;
  uptime?: number;
};

export function ReportItem({ date, worstStatus, uptime }: ReportItemProps) {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  return (
    <Popover
      title={date}
      content={
        <div>
          <p className="flex justify-between gap-2">
            Worst status: <span>{worstStatus ?? "—"}</span>
          </p>
          <p className="flex justify-between gap-4">
            Uptime: <span>{uptime ? `${uptime}%` : "—"}</span>
          </p>
        </div>
      }
    >
      <div
        className={cn(
          ITEM_CLASS_NAME,
          worstStatus === undefined && "bg-gray-300",
          worstStatus === undefined && isDarkMode && "bg-gray-500",
          worstStatus === "outage"
            ? "bg-red-500"
            : worstStatus === "degraded"
              ? "bg-yellow-500"
              : worstStatus === "operational" && "bg-green-500",
        )}
      />
    </Popover>
  );
}
