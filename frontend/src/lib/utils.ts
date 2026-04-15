import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function appContainer(): HTMLElement | null | undefined {
  return typeof document === "undefined"
    ? undefined
    : document.getElementById("root");
}

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

export function mapDate(value: string): string {
  const date = new Date(value);
  const options: Intl.DateTimeFormatOptions = {
    day: "numeric",
    month: "long",
    year: "numeric",
  };
  return date.toLocaleDateString("en-us", options);
}
