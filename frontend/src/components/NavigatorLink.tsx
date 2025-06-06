function NavigatorLink({
  text,
  url,
  navigate,
}: {
  text: string;
  url?: string;
  navigate: (url?: string) => () => void;
}) {
  return (
    <a
      className={`underline ${
        !url
          ? 'opacity-50 pointer-events-none cursor-default'
          : 'cursor-pointer'
      }`}
      onClick={navigate(url)}
    >
      {text}
    </a>
  );
}

export default NavigatorLink;
