import type { Config } from "vike/types";
import vikeReact from "vike-react/config";
import vikeReactQuery from "vike-react-query/config";

// Default config (can be overridden by pages)
// https://vike.dev/config

export default {
  // https://vike.dev/head-tags
  title: "mrdsx observer",
  extends: [vikeReact, vikeReactQuery],
} satisfies Config;
