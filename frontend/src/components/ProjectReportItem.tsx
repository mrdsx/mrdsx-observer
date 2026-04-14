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
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger
        nativeButton={false}
        render={
          // biome-ignore lint/a11y/noStaticElementInteractions: rm -rf /
          <div
            className="group outline-0"
            onMouseEnter={() => setIsOpen(true)}
            onMouseLeave={() => setIsOpen(false)}
          >
            <div
              className={cn(
                "h-6 w-2 rounded duration-50",
                isOpen && "-translate-y-1",
                worstStatus === undefined && "bg-gray-300 dark:bg-gray-500",
                worstStatus === "outage"
                  ? "bg-red-500"
                  : worstStatus === "degraded"
                    ? "bg-yellow-500"
                    : worstStatus === "operational" && "bg-green-500",
              )}
            />
          </div>
        }
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
