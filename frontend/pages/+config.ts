import type { Config } from "vike/types";
import vikeSolid from "vike-solid/config";

// Default config (can be overridden by pages)
// https://vike.dev/config

export default {
  title: "mrdsx observer",
  extends: [vikeSolid],
  server: true,
} satisfies Config;
