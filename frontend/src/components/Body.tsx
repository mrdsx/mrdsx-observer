import { cn } from "@/lib/utils";
import { useThemeStore } from "@/stores/theme";

export function Body({ children }: React.PropsWithChildren) {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  return <body className={cn(isDarkMode && "dark")}>{children}</body>;
}
