import { ChevronDownIcon } from '@heroicons/react/16/solid';

import type { SeqDetail, SeqInfo } from '../types/sequence.ts';
import * as React from 'react';

export default function Search({
  seq,
  handleSelect,
  handleInput,
  pattern,
  seqSelect,
}: {
  pattern?: string;
  seq: SeqInfo & SeqDetail;
  handleSelect: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  handleInput: (e: React.ChangeEvent<HTMLInputElement>) => void;
  seqSelect?: string;
}) {
  return (
    <div>
      <div className="mt-2">
        <div className="h-12 w-120 flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 has-[input:focus-within]:outline-2 has-[input:focus-within]:-outline-offset-2 has-[input:focus-within]:outline-blue-600">
          <input
            value={pattern}
            id="price"
            name="price"
            type="text"
            placeholder="input regex string"
            className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
            onChange={handleInput}
          />
          <div className="grid shrink-0 grid-cols-1 focus-within:relative">
            <select
              value={seqSelect}
              id="nucleotide"
              name="nucleotide"
              aria-label="nucleotide"
              className="h-12 bg-gray-100 col-start-1 row-start-1 w-full appearance-none rounded-md py-1.5 pr-7 pl-3 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-600 sm:text-sm/6"
              onChange={handleSelect}
              defaultValue={''}
            >
              <option value={''} disabled hidden>
                Choose nucleotide
              </option>
              <option value={seq.id}>{seq.orgname}</option>
            </select>
            <ChevronDownIcon
              aria-hidden="true"
              className="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
