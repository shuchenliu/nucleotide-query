import { useMutation } from '@tanstack/react-query';
import { ENDPOINTS } from './constants.ts';
import type { Payload } from '../types/result.ts';

export const useRegexQuery = () =>
  useMutation({
    mutationFn: async (payload: Payload) => {
      // validate pattern

      let res;
      let params;
      if ('url' in payload) {
        params = new URLSearchParams(payload.url);
        res = await fetch(payload.url);
      } else {
        params = new URLSearchParams({
          page_size: '10',
          ...payload,
        });

        res = await fetch(ENDPOINTS.QUERY + '?' + params.toString());
      }

      if (!res.ok) {
        // throws an error that will be caught by react-query
        throw new Error(`${res.status}`);
      }

      const data = await res.json();

      return {
        data,
        pattern: params.get('pattern'),
      };
    },
  });
