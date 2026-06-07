import { Header } from "@/components/Header";
import "@/globals.css";
import { createEffect, onMount, type ParentProps } from "solid-js";
import { initTheme, isDarkMode } from "@/stores/theme";

export default function RootLayout(props: ParentProps) {
  onMount(() => {
    initTheme();
  });

  createEffect(() => {
    document.body.setAttribute("data-kb-theme", isDarkMode() ? "dark" : "");
  });

  return (
    <>
      <Header />
      <main class="flex w-full max-w-300 flex-col px-4 py-8">
        {props.children}
      </main>
    </>
  );
}
