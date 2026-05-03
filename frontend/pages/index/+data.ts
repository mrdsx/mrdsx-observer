import type { PageContextServer } from "vike/types";
import { apiFetch } from "@/lib/api";
import { STATUS_CODES } from "@/lib/constants";
import { type ProjectsReports, projectsReportsSchema } from "@/lib/schemas";
import type { UseDataResult } from "@/lib/types";

export async function data(
  _pageContext: PageContextServer,
): Promise<UseDataResult<ProjectsReports>> {
  try {
    const response = await apiFetch("/api/projects");
    const data = await response.json();

    const { data: projectsData, success } =
      projectsReportsSchema.safeParse(data);
    if (!success) {
      return {
        success: false,
        code: STATUS_CODES.INVALID_RESPONSE,
        data: null,
      };
    }

    return { success: true, code: STATUS_CODES.OK, data: projectsData };
  } catch (error) {
    console.error(error);
    return { success: false, code: STATUS_CODES.INTERNAL_ERROR, data: null };
  }
}

export type Data = Awaited<ReturnType<typeof data>>;
