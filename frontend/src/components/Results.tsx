import type { Payload, Result } from '../types/result.ts';
import Location from './Location.tsx';
import { useEffect, useMemo, useState } from 'react';
import type { UseMutateFunction } from '@tanstack/react-query';
import NavigatorLink from './NavigatorLink.tsx';

function getPageList(current: number, total: number): number[] {
  const pageCount = Math.min(5, total);
  let start = Math.max(1, current - 2);
  let end = start + pageCount - 1;

  if (end > total) {
    end = total;
    start = Math.max(1, end - pageCount + 1);
  }

  const pages: number[] = [];
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }

  return pages;
}

function Results({
  data,
  sequence,
  mutate,
  pattern,
}: {
  data: Result;
  sequence: string;
  mutate: UseMutateFunction<any, Error, Payload, unknown>;
  pattern?: string | null;
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

  const pagelist = useMemo(() => {
    if (!displayData) {
      return [-1];
    }

    return getPageList(displayData.current_page, displayData.total_pages);
  }, [displayData]);

  if (!displayData) {
    return null;
  }

  const navigate = (url?: string) => () => {
    console.log(url);

    if (url) {
      mutate({
        url,
      });
    }
  };

  const navigateToPage =
    (pattern: string, pageSize: string, page: string) => () => {
      mutate({
        pattern,
        page_size: pageSize,
        page,
      });
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
        {['previous', ...pagelist, 'next'].map((key) => {
          if (typeof key === 'string') {
            return (
              <NavigatorLink
                key={key}
                navigate={navigate(
                  displayData[key as keyof typeof displayData] as string,
                )}
                canNavigate={!!displayData[key as keyof typeof displayData]}
                text={key.slice(0, 4)}
              />
            );
          }

          return (
            <NavigatorLink
              key={'pagelink' + key}
              navigate={navigateToPage(
                pattern!,
                displayData?.page_size + '',
                key + '',
              )}
              canNavigate={key != displayData.current_page}
              text={key + ''}
            />
          );
        })}
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
