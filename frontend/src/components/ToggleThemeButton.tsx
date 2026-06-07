import { MoonIcon, SunIcon } from "lucide-solid";
import { Show } from "solid-js";
import { isDarkMode, toggleTheme } from "@/stores/theme";
import { Button } from "./ui/button";

export function ToggleThemeButton() {
  return (
    <Button size="icon" variant="outline" onClick={toggleTheme}>
      <Show when={isDarkMode()}>
        <SunIcon />
      </Show>
      <Show when={!isDarkMode()}>
        <MoonIcon />
      </Show>
    </Button>
  );
}
