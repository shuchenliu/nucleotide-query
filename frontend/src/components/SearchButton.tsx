import type { UseMutateFunction } from '@tanstack/react-query';
import type { Payload } from '../types/result.ts';

function SearchButton({
  pattern,
  nucId,
  mutate,
  pageSize,
}: {
  pattern?: string;
  nucId?: string;
  pageSize?: string;
  mutate: UseMutateFunction<any, Error, Payload, unknown>;
}) {
  const onClick = () => {
    if (pattern) {
      mutate({ pattern, page_size: pageSize });
    }
  };

  return (
    <div className={'ml-3'}>
      <button
        onClick={onClick}
        disabled={!pattern || !nucId}
        className="h-12 w-30 disabled:bg-gray-200 bg-blue-200 hover:bg-blue-100 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center justify-center"
      >
        <span>GO</span>
      </button>
    </div>
  );
}

export default SearchButton;
