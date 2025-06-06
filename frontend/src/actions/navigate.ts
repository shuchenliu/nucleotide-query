export const navigate = (mutate: any, url?: string) => () => {
  if (url) {
    mutate({
      url,
    });
  }
};

export const navigateToPage =
  (mutate: any, pattern: string, pageSize: string, page: string) => () => {
    mutate({
      pattern,
      page_size: pageSize,
      page,
    });
  };

export const navigateSearch =
  (mutate: any, pattern: string, pageSize = '10') =>
  () => {
    mutate({
      pattern,
      page_size: pageSize,
    });
  };
