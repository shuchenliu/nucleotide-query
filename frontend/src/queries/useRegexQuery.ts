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

        console.log(params.toString());

        res = await fetch(ENDPOINTS.QUERY + '?' + params.toString());
      }

      const data = await res.json();

      return {
        data,
        pattern: params.get('pattern'),
      };
    },
  });
