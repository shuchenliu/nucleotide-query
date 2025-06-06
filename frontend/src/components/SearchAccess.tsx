import NavigatorLink from './NavigatorLink.tsx';
import { navigateSearch } from '../actions/navigate.ts';
import type { Search } from '../types/search.ts';

function SearchAccess({
  searchArray,
  pageSize,
  mutate,
  text,
  sideEffect,
}: {
  mutate: any;
  searchArray?: Array<Search>;
  pageSize?: string;
  text: string;
  sideEffect?: any;
}) {
  if (!searchArray || searchArray.length === 0) {
    return null;
  }

  return (
    <div className={'flex flex-row flex-wrap'}>
      <div>{text}</div>
      {searchArray.map(({ pattern: currentPattern }) => (
        <div key={currentPattern} className={'ml-2'}>
          <NavigatorLink
            text={currentPattern}
            canNavigate={true}
            navigate={() => {
              if (sideEffect) {
                sideEffect(currentPattern);
              }

              navigateSearch(mutate, currentPattern, pageSize)();
            }}
          />
        </div>
      ))}
    </div>
  );
}

export default SearchAccess;
