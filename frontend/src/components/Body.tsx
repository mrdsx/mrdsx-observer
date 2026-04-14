"use client";

import { cn } from "@/lib/utils";
import { useThemeStore } from "@/stores/themeStore";

export function Body({ children }: React.PropsWithChildren) {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  return (
    <body
      className={cn(
        "flex min-h-screen flex-col items-center",
        isDarkMode && "dark",
      )}
    >
      {children}
    </body>
  );
}
