import { MetaProvider, Title } from "@solidjs/meta";
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { createEffect, onMount, Suspense } from "solid-js";
import "./globals.css";
import { Header } from "./components/Header";
import { initTheme, isDarkMode } from "./stores/theme";

export default function App() {
  onMount(() => {
    initTheme();
  });

  createEffect(() => {
    document.body.setAttribute("data-kb-theme", isDarkMode() ? "dark" : "");
  });

  return (
    <Router
      root={(props) => (
        <MetaProvider>
          <Title>mrdsx observer</Title>
          <Suspense>
            <Header />
            <main class="flex w-full max-w-300 flex-col px-4 py-8">
              {props.children}
            </main>
          </Suspense>
        </MetaProvider>
      )}
    >
      <FileRoutes />
    </Router>
  );
}
