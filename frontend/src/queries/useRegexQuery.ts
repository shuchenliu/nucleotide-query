import { useMutation } from '@tanstack/react-query';
import { ENDPOINTS } from './constants.ts';
import type { Payload } from '../types/result.ts';

export const useRegexQuery = () =>
  useMutation({
    mutationFn: async (payload: Payload) => {
      // validate pattern

      let res;
      if ('url' in payload) {
        res = await fetch(payload.url);
      } else {
        const params = new URLSearchParams({
          page_size: '10',
          ...payload,
        });
        res = await fetch(ENDPOINTS.QUERY + '?' + params.toString());
      }

      return await res.json();
    },
  });

export const useNavigate = () =>
  useMutation({
    mutationFn: async (url: string) => {
      // validate pattern
      const res = await fetch(url);
      return await res.json();
    },
  });
