function NavigatorLink({
  canNavigate,
  text,
  navigate,
}: {
  text: string;
  canNavigate: boolean;
  navigate: () => unknown;
}) {
  return (
    <a
      className={`${
        !canNavigate
          ? 'opacity-20 pointer-events-none cursor-default'
          : 'cursor-pointer underline'
      }`}
      onClick={navigate}
    >
      {text}
    </a>
  );
}

export default NavigatorLink;
