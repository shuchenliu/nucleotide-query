import type { Result } from '../types/result.ts';
import Location from './Location.tsx';
import { useMemo } from 'react';

function Results({ data, sequence }: { data: Result; sequence: string }) {
  if (!data) {
    return null;
  }

  const indexStart = useMemo(
    () => (data.current_page - 1) * data.page_size + 1,
    [data.page_size, data.current_page],
  );

  return (
    <div>
      <div className={'w-full flex flex-row items-center justify-between h-10'}>
        {['#', 'start', 'end'].map((label) => (
          <div
            key={label}
            className={
              'w-20 flex flex-row items-center justify-center text-xl font-medium'
            }
          >
            {label}
          </div>
        ))}
        <div className={'flex-1 text-xl font-medium'}>sequence</div>
      </div>
      <div
        className={'w-full bg-gray-100 shadow-md rounded-xl overflow-hidden'}
      >
        {data.results.map(({ start, end }, index) => (
          <div
            key={'match' + index}
            className={`flex flex-row items-center justify-between h-10 w-full  ${
              index % 2 == 1 ? 'bg-white' : 'transparent'
            }`}
          >
            {[indexStart + index, start, end].map((num) => (
              <div
                key={`${index}-${num}`}
                className={'flex flex-row items-center justify-center w-20'}
              >
                {num}
              </div>
            ))}

            <Location start={start} end={end} sequence={sequence} />
          </div>
        ))}
      </div>

      <div>
        <div className={'pt-8'}>
          showing {indexStart} - {indexStart + data.results.length} {' of '}{' '}
          {data.count} {data.count === 1 ? 'match' : 'matches'}
        </div>
      </div>
    </div>
  );
}

export default Results;
