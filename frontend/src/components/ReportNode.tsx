import { cn } from "@/lib/utils";
import { useThemeStore } from "@/stores/themeStore";

const NODE_CLASS_NAME = "w-2 h-6 rounded";

export function ReportNode({ status }: { status: string }) {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  if (status === "outage") {
    return <div className={cn(NODE_CLASS_NAME, "bg-red-500")} />;
  }

  if (status === "degraded") {
    return <div className={cn(NODE_CLASS_NAME, "bg-yellow-500")} />;
  }

  if (status === "unknown") {
    return (
      <div
        className={cn(
          NODE_CLASS_NAME,
          "bg-gray-300",
          isDarkMode && "bg-gray-600",
        )}
      />
    );
  }

  return <div className={cn(NODE_CLASS_NAME, "bg-green-500")} />;
}
