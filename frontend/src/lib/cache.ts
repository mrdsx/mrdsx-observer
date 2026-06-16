type CachedProps<TData> = {
  fetchFn: () => TData | Promise<TData>;
  fetchKey: string;
};

// Whatever number I put - it just looked good to me
// (30 seconds but in milliseconds)
const STALE_TIME = 30 * 1000;
const cache: Record<string, { result: unknown; revalidateAt: Date }> = {};

function getRevalidationTime(date: Date): Date {
  return new Date(date.getTime() + STALE_TIME);
}

/*
 * Stale-while-revalidate caching
 */
export async function cached<TData>({ fetchFn, fetchKey }: CachedProps<TData>) {
  const cachedData = cache[fetchKey];
  if (cachedData === undefined) {
    const result = await fetchFn();
    const now = new Date();
    cache[fetchKey] = {
      result,
      revalidateAt: getRevalidationTime(now),
    };

    return result;
  }

  setTimeout(async () => {
    const result = await fetchFn();
    const now = new Date();
    if (cachedData.revalidateAt <= now) {
      cache[fetchKey] = {
        result,
        revalidateAt: getRevalidationTime(now),
      };
    }
  });

  return cachedData.result as TData;
}
