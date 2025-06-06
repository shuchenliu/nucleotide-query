import * as React from 'react';

function PageSizeSelect({
  handleSelect,
  pageSize,
}: {
  handleSelect: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  pageSize?: string;
}) {
  return (
    <form className="max-w-sm mx-auto">
      <select
        value={pageSize}
        id="page-size"
        onChange={handleSelect}
        className="h-12 ml-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <option selected>results per page</option>
        <option value="10">10</option>
        <option value="50">50</option>
        <option value="100">100</option>
        <option value="200">200</option>
        <option value="500">500</option>
      </select>
    </form>
  );
}

export default PageSizeSelect;
