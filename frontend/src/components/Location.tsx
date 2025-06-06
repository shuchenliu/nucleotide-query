const pos = 5;
function Location({
  start,
  end,
  sequence,
}: {
  start: number;
  end: number;
  sequence: string;
}) {
  return (
    <div className={'flex-1 items-center justify-center overflow-hidden'}>
      {start > 0 && (
        <span>{sequence.slice(Math.max(0, start - pos), start)}</span>
      )}
      <span className={'text-red-500'}>{sequence.slice(start, end)}</span>

      {end < sequence.length - 1 && (
        <span>{sequence.slice(end, Math.min(sequence.length, end + pos))}</span>
      )}
    </div>
  );
}

export default Location;
