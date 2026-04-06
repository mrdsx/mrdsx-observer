"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ConfigProvider, theme } from "antd";
import { useThemeStore } from "@/stores/themeStore";

const queryClient = new QueryClient();

export function AppProvider({ children }: React.PropsWithChildren) {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={{
          algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
        }}
      >
        {children}
      </ConfigProvider>
    </QueryClientProvider>
  );
}
