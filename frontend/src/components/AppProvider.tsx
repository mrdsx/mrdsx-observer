"use client";

import { ConfigProvider, theme } from "antd";
import { useThemeStore } from "@/stores/themeStore";

export function AppProvider({ children }: React.PropsWithChildren) {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  return (
    <ConfigProvider
      theme={{
        algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
      }}
    >
      {children}
    </ConfigProvider>
  );
}
