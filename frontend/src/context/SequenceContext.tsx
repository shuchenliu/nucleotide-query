import { createContext } from 'react';
import type { SeqDetail, SeqInfo } from '../types/sequence.ts';

const SequenceContext = createContext<SeqDetail & SeqInfo>(
  {} as SeqDetail & SeqInfo,
);

export default SequenceContext;
