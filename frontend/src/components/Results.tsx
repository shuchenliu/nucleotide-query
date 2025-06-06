import type { Result } from '../types/result.ts';
import Location from './Location.tsx';

function Results({ data, sequence }: { data: Result; sequence: string }) {
  if (!data) {
    return null;
  }

  return (
    <div>
      <div className={'w-full flex flex-row items-center justify-between h-10'}>
        <div
          className={
            'w-20 flex flex-row items-center justify-center text-xl font-medium'
          }
        >
          start
        </div>
        <div
          className={
            'w-20 flex flex-row items-center justify-center text-xl font-medium'
          }
        >
          end
        </div>
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
            {[start, end].map((num) => (
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
    </div>
  );
}

export default Results;
