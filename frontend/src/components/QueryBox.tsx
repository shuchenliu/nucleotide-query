import { useContext, useState } from 'react';
import sequenceContext from '../context/SequenceContext.tsx';
import Search from './Search.tsx';
import SearchButton from './SearchButton.tsx';
import * as React from 'react';
import { useRegexQuery } from '../queries/useRegexQuery.ts';
import Results from './Results.tsx';

function QueryBox() {
  const sequence = useContext(sequenceContext);

  const [selected, setSelected] = useState<string>();
  const [pattern, setPattern] = useState<string>();

  const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelected(e.target.value);
  };

  const handInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPattern(e.target.value);
  };

  const { data, mutate } = useRegexQuery();

  return (
    <div>
      <div className={'py-10 flex flex-row items-baseline'}>
        <Search
          seq={sequence}
          handleSelect={handleSelect}
          handleInput={handInput}
        />
        <SearchButton pattern={pattern} nucId={selected} mutate={mutate} />
      </div>
      <Results data={data} sequence={sequence.sequence} />
    </div>
  );
}

export default QueryBox;
