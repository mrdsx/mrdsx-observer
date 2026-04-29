import { BACKEND_URL } from "../server/constants";

export async function apiFetch(url: `/${string}`) {
  return await fetch(`${BACKEND_URL}${url}`);
}
