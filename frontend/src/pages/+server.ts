import vike from "vike/fetch";
import type { Server } from "vike/types";

export default {
  fetch: (request: Request) => {
    // @ts-expect-error rm -rf /
    return vike.fetch(request);
  },
} satisfies Server;
