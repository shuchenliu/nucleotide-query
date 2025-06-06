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
};
