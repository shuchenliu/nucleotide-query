import './App.css';
import { useSequenceString } from './queries/useSequenceString.ts';
import SequenceContext from './context/SequenceContext.tsx';

function App() {
  const { data, isSuccess } = useSequenceString();

  if (!isSuccess) {
    return null;
  }

  return (
    <SequenceContext.Provider value={data}>
      <h1>Nucleotide query</h1>
    </SequenceContext.Provider>
  );
}

export default App;
