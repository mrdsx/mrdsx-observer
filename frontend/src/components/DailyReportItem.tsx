import { createSignal } from "solid-js";
import { cx } from "@/lib/cva";
import { dateToLocaleDateString } from "@/lib/utils";
import {
  Popover,
  PopoverArrow,
  PopoverContent,
  PopoverTrigger,
} from "./ui/popover";

type ReportItemProps = Partial<{
  date: string;
  worstStatus: string;
  uptime: number;
}>;

export function DailyReportItem({
  date,
  worstStatus,
  uptime,
}: ReportItemProps) {
  const [open, setOpen] = createSignal<boolean>(false);

  return (
    <Popover gutter={0} open={open()} onOpenChange={setOpen}>
      <PopoverTrigger
        class="group outline-0"
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
      >
        <div
          class={cx(
            "h-6 w-2 rounded group-hover:-translate-y-0.75 duration-50 outline-0",
            open() ? "-translate-y-0.75" : "group-hover:translate-y-0",
            worstStatus === undefined && "bg-gray-300 dark:bg-gray-500",
            worstStatus === "outage"
              ? "bg-red-500"
              : worstStatus === "degraded"
                ? "bg-yellow-500"
                : worstStatus === "operational" && "bg-green-500",
          )}
        />
      </PopoverTrigger>
      <PopoverContent class="max-w-50">
        <PopoverArrow />
        <span class="font-semibold mb-2">
          {date !== undefined && dateToLocaleDateString(date)}
        </span>
        <div class="text-muted-foreground">
          <p>Status: {worstStatus ?? "-"}</p>
          <p>Uptime: {uptime === undefined ? "-" : `${uptime}%`}</p>
        </div>
      </PopoverContent>
    </Popover>
  );
}
