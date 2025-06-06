import { useMutation } from '@tanstack/react-query';
import { ENDPOINTS } from './constants.ts';

export const useRegexQuery = () =>
  useMutation({
    mutationFn: async (pattern: string) => {
      // validate pattern

      const params = new URLSearchParams({
        pattern: pattern,
        page_size: '10',
      });
      const res = await fetch(ENDPOINTS.QUERY + '?' + params.toString());
      return await res.json();
    },
  });
