import { useContext } from 'react';
import sequenceContext from '../context/SequenceContext.tsx';
import Search from './Search.tsx';
import SearchButton from './SearchButton.tsx';

function QueryBox() {
  const sequence = useContext(sequenceContext);

  return (
    <div className={'py-10 flex flex-row items-baseline'}>
      {/*<NucleotideSelect seq={sequence} />*/}
      <Search seq={sequence} />
      <SearchButton />
    </div>
  );
}

export default QueryBox;
