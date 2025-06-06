export type Match = {
  id: 'string';
  start: number;
  end: number;
};

export type Result = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Array<Match>;
  total_pages: number;
  current_page: number;
  page_size: 10;
};

export type Payload =
  | {
      pattern: string;
      page_size?: string;
      page?: string;
    }
  | {
      url: string;
    };
