import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { REPORTS_WINDOW_DAYS } from "./constants";
import type { DailyReport, Project } from "./schemas";

export function appContainer(): HTMLElement | null | undefined {
  return typeof document === "undefined"
    ? undefined
    : document.getElementById("root");
}

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

export function dateToLocaleDateString(value: string): string {
  const date = new Date(value);
  const options: Intl.DateTimeFormatOptions = {
    day: "numeric",
    month: "long",
    year: "numeric",
  };

  return date.toLocaleDateString("en-us", options);
}

export function dateToISOString(date: Date): string {
  const year = date.getFullYear().toString();
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");

  return `${year}-${month}-${day}`;
}

/**
 * Maps reports to the list of reports for the last 30 days.
 * Empty reports are mapped to undefined.
 */
export function mapReports(
  reports: Project["dailyReports"],
): (Partial<DailyReport> | undefined)[] {
  const result: (Partial<DailyReport> | undefined)[] =
    Array(REPORTS_WINDOW_DAYS).fill(undefined);
  const datesSet = new Set(reports.map((report) => report.date));

  const latestDate = new Date();

  for (let i = 0; i < REPORTS_WINDOW_DAYS; i++) {
    const currentDate = new Date(
      latestDate.getFullYear(),
      latestDate.getMonth(),
      latestDate.getDate() - i,
    );

    if (datesSet.has(dateToISOString(currentDate))) {
      result[i] = reports.find(
        (report) => report.date === dateToISOString(currentDate),
      );
    } else {
      result[i] = {
        date: dateToISOString(currentDate),
        worstStatus: undefined,
        uptime: undefined,
      };
    }
  }

  return result.toReversed();
}
