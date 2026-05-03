import type { STATUS_CODES } from "./constants";

export type UseDataResult<TData> =
  | { success: true; code: typeof STATUS_CODES.OK; data: TData }
  | { success: false; code: string; data: null };
