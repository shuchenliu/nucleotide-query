import { useQuery } from '@tanstack/react-query';
import type { SeqDetail, SeqInfo } from '../types/sequence.ts';
import { ENDPOINTS } from './constants.ts';

export const useSequenceString = () =>
  useQuery<SeqDetail & SeqInfo>({
    queryKey: ['sequence-string'],
    queryFn: async () => {
      const res = await fetch(ENDPOINTS.SEQUENCE);
      const seqArray: Array<SeqInfo> = await res.json();
      const seqInfo = seqArray[0];

      const sequenceResponse = await fetch(
        `${ENDPOINTS.SEQUENCE}${seqInfo.id}`,
      );
      const data: SeqDetail = await sequenceResponse.json();
      return {
        ...data,
        ...seqInfo,
      };
    },
  });
