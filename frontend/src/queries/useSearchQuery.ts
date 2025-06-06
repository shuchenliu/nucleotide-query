import { useQuery } from '@tanstack/react-query';
import { ENDPOINTS } from './constants.ts';
import type { Search } from '../types/search.ts';

const makeQuery = (queryKey: string, endpoint: string) => () =>
  useQuery<Array<Search>>({
    queryKey: [queryKey],
    queryFn: async () => {
      const res = await fetch(endpoint);
      const searchArray: Array<Search> = await res.json();
      return searchArray;
    },
    staleTime: 0,
    refetchOnMount: true,
  });

export const useRecentSearch = makeQuery(
  'recent_search',
  ENDPOINTS.RECENT_SEARCH,
);

export const useFrequentSearch = makeQuery(
  'frequent_search',
  ENDPOINTS.FREQUENT_SEARCH,
);
