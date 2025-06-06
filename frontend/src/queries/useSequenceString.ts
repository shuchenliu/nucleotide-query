import { useQuery } from '@tanstack/react-query';
import type { SeqDetail, SeqInfo } from '../types/sequence.ts';

export const useSequenceString = () =>
  useQuery<SeqDetail>({
    queryKey: ['sequence-string'],
    queryFn: async () => {
      const res = await fetch('/api/sequence/');
      const seqArray: Array<SeqInfo> = await res.json();
      const seqInfo = seqArray[0];

      const sequenceResponse = await fetch(`/api/sequence/${seqInfo.id}`);
      const data: SeqDetail = await sequenceResponse.json();
      return data;
    },
  });
