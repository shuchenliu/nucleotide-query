import { createContext } from 'react';
import type { SeqDetail } from '../types/sequence.ts';

const SequenceContext = createContext<SeqDetail>({} as SeqDetail);

export default SequenceContext;
