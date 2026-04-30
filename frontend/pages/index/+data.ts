import type { PageContextServer } from "vike/types";
import { apiFetch } from "../../src/lib/api";
import { projectsReportsSchema } from "../../src/lib/schemas";

export async function data(_pageContext: PageContextServer) {
  try {
    const response = await apiFetch("/api/projects");
    const data = await response.json();

    const { data: projectsData, success } =
      projectsReportsSchema.safeParse(data);
    if (!success) {
      return { success: false, code: "INVALID_RESPONSE" };
    }

    return { success: true, data: projectsData };
  } catch (error) {
    console.error(error);
    return { success: false, code: "INTERNAL_ERROR" };
  }
}

export type Data = Awaited<ReturnType<typeof data>>;
