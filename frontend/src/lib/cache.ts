type CachedProps<TData> = {
  fetchFn: () => TData | Promise<TData>;
  fetchKey: string;
};

const cache: Record<string, unknown> = {};

export async function cached<TData>({ fetchFn, fetchKey }: CachedProps<TData>) {
  const cachedData = cache[fetchKey];
  if (cachedData === undefined) {
    const result = await fetchFn();
    cache[fetchKey] = result;
    return result;
  }

  setTimeout(async () => {
    const result = await fetchFn();
    cache[fetchKey] = result;
  });

  return cachedData as TData;
}
