import { useSWRConfig, MutatorOptions } from "swr";

interface GlobalCacheHook {
  getItem: <TValue = any>(key: string) => TValue | undefined;
  setItem: <TValue = any>(
    key: string,
    value: TValue,
    options?: boolean | MutatorOptions<TValue>
  ) => Promise<TValue | undefined>;
  refreshItem: <TValue = any>(key: string) => Promise<TValue | undefined>;
  deleteItem: (key: string) => void;
}

export default function useGlobalCache(): GlobalCacheHook {
  const { cache, mutate } = useSWRConfig();

  const getItem = <TValue = any>(key: string): TValue | undefined => {
    return cache.get(key)?.data;
  };

  const setItem = async <TValue = any>(
    key: string,
    value: TValue,
    options?: boolean | MutatorOptions<TValue>
  ): Promise<TValue | undefined> => {
    return await mutate(key, value, options);
  };

  const refreshItem = async <TValue = any>(
    key: string
  ): Promise<TValue | undefined> => {
    return await mutate(key);
  };

  const deleteItem = (key: string): void => {
    cache.delete(key);
  };

  return {
    getItem,
    setItem,
    refreshItem,
    deleteItem,
  };
}
