import type { Payload, Result } from '../types/result.ts';
import Location from './Location.tsx';
import { useEffect, useMemo, useState } from 'react';
import type { UseMutateFunction } from '@tanstack/react-query';
import NavigatorLink from './NavigatorLink.tsx';

function Results({
  data,
  sequence,
  mutate,
}: {
  data: Result;
  sequence: string;
  mutate: UseMutateFunction<any, Error, Payload, unknown>;
}) {
  const [displayData, setDisplayData] = useState<Result | null>(data);

  useEffect(() => {
    if (data) {
      setDisplayData(data);
    }
  }, [data]);

  const indexStart = useMemo(() => {
    if (!displayData) {
      return -1;
    }
    return (displayData.current_page - 1) * displayData.page_size + 1;
  }, [displayData]);

  if (!displayData) {
    return null;
  }

  const navigate = (url?: string) => () => {
    if (url) {
      mutate({
        url,
      });
    }
  };

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
        {displayData.results.map(({ start, end }, index) => (
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

      <div
        className={
          'w-full px-10 flex flex-row items-center justify-between mt-5'
        }
      >
        {['previous', 'next'].map((key) => (
          <NavigatorLink
            key={key}
            navigate={navigate}
            url={displayData[key as keyof typeof displayData] as string}
            text={key.slice(0, 4)}
          />
        ))}
      </div>

      <div className={'pt-8'}>
        showing {indexStart} - {indexStart + displayData.results.length - 1}{' '}
        {' of '} {displayData.count}{' '}
        {displayData.count === 1 ? 'match' : 'matches'}
      </div>
    </div>
  );
}

export default Results;
