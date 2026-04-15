import { useState } from "react";
import { cn, mapDate } from "@/lib/utils";
import {
  Popover,
  PopoverContent,
  PopoverHeader,
  PopoverTitle,
  PopoverTrigger,
} from "./ui/popover";

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
  const [open, setOpen] = useState<boolean>(false);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger
        className={cn(
          "h-6 w-2 rounded duration-50 outline-0",
          open && "-translate-y-1",
          worstStatus === undefined && "bg-gray-300 dark:bg-gray-500",
          worstStatus === "outage"
            ? "bg-red-500"
            : worstStatus === "degraded"
              ? "bg-yellow-500"
              : worstStatus === "operational" && "bg-green-500",
        )}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
      />
      {/* DO NOT REMOVE `sideOffset` */}
      {/* Removing it will result in layout flicker when hovering from bottom */}
      <PopoverContent className="max-w-50" sideOffset={10}>
        <PopoverHeader>
          <PopoverTitle>{date !== undefined && mapDate(date)}</PopoverTitle>
          <div className="text-muted-foreground">
            <p>Status: {worstStatus === undefined ? "-" : worstStatus}</p>
            <p>Uptime: {uptime === undefined ? "-" : `${uptime}%`}</p>
          </div>
        </PopoverHeader>
      </PopoverContent>
    </Popover>
  );
}
