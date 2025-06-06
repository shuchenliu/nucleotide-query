import { useContext, useState } from 'react';
import sequenceContext from '../context/SequenceContext.tsx';
import Search from './Search.tsx';
import SearchButton from './SearchButton.tsx';
import * as React from 'react';
import { useRegexQuery } from '../queries/useRegexQuery.ts';
import Results from './Results.tsx';
import PageSizeSelect from './PageSizeSelect.tsx';
import {
  useFrequentSearch,
  useRecentSearch,
} from '../queries/useSearchQuery.ts';

import SearchAccess from './SearchAccess.tsx';

function QueryBox() {
  const sequence = useContext(sequenceContext);

  const [selected, setSelected] = useState<string>();
  const [selectedPageSize, setSelectedPageSize] = useState<string>();
  const [pattern, setPattern] = useState<string>();

  const { data: recentSearch } = useRecentSearch();
  const { data: frequentSearch } = useFrequentSearch();

  const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelected(e.target.value);
  };

  const handlePageSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedPageSize(e.target.value);
  };

  const handInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPattern(e.target.value);
  };

  const { data, mutate, isError, error } = useRegexQuery();

  return (
    <div>
      <div className={'py-5 flex flex-row items-baseline'}>
        <Search
          pattern={pattern}
          seq={sequence}
          handleSelect={handleSelect}
          handleInput={handInput}
          seqSelect={selected}
        />
        <PageSizeSelect handleSelect={handlePageSelect} />
        <SearchButton
          pattern={pattern}
          nucId={selected}
          mutate={mutate}
          pageSize={selectedPageSize}
        />
      </div>
      <SearchAccess
        text={'recent searches'}
        mutate={mutate}
        searchArray={recentSearch}
        pageSize={selectedPageSize}
        sideEffect={setPattern}
      />
      <SearchAccess
        text={'most frequent searches'}
        mutate={mutate}
        searchArray={frequentSearch}
        pageSize={selectedPageSize}
        sideEffect={setPattern}
      />
      {isError ? (
        <div className={'h-60 w-full flex justify-center items-center'}>
          <p className={'text-2xl'}>
            {error.message == '404'
              ? 'No match found'
              : 'Something wrong. Please try again.'}
          </p>
        </div>
      ) : (
        <Results
          data={data?.data}
          sequence={sequence.sequence}
          mutate={mutate}
          pattern={data?.pattern}
        />
      )}
    </div>
  );
}

export default QueryBox;
