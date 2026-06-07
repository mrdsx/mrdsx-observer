import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import vike from "vike/plugin";
import vikeSolid from "vike-solid/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vike(), vikeSolid(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
