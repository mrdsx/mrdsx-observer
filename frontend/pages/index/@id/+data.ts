import type { PageContextServer } from "vike/types";
import { apiFetch } from "@/lib/api";
import { STATUS_CODES } from "@/lib/constants";
import { type ServicesReports, servicesReportsSchema } from "@/lib/schemas";
import type { UseDataResult } from "@/lib/types";

export async function data(
  pageContext: PageContextServer,
): Promise<UseDataResult<ServicesReports>> {
  try {
    const projectId = pageContext.routeParams.id;
    const response = await apiFetch(`/api/projects/${projectId}`);
    const data = await response.json();

    if (response.status === 404) {
      return {
        success: false,
        code: STATUS_CODES.NOT_FOUND,
        data: null,
      };
    }

    const { data: servicesData, success } =
      servicesReportsSchema.safeParse(data);
    if (!success) {
      return {
        success: false,
        code: STATUS_CODES.INVALID_RESPONSE,
        data: null,
      };
    }

    return { success: true, code: STATUS_CODES.OK, data: servicesData };
  } catch (error) {
    console.error(error);
    return { success: false, code: STATUS_CODES.INTERNAL_ERROR, data: null };
  }
}

export type Data = Awaited<ReturnType<typeof data>>;
