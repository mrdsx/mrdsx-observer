"use client";

import { MoonIcon, SunIcon } from "lucide-react";
import { useThemeStore } from "@/stores/themeStore";
import { Button } from "./ui/button";

export function ToggleThemeButton() {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);
  const toggleTheme = useThemeStore((state) => state.toggleTheme);

  return (
    <Button size="lg" variant="outline" onClick={toggleTheme}>
      {isDarkMode ? <SunIcon /> : <MoonIcon />}
    </Button>
  );
}
