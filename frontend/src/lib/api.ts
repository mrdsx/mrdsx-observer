import { API_URL } from "./constants";

export async function apiFetch(url: `/${string}`) {
  return await fetch(`${API_URL}${url}`);
}
