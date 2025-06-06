import './App.css';
import { useSequenceString } from './queries/useSequenceString.ts';
import SequenceContext from './context/SequenceContext.tsx';
import QueryBox from './components/QueryBox.tsx';

function App() {
  const { data, isSuccess } = useSequenceString();

  if (!isSuccess) {
    return null;
  }

  return (
    <SequenceContext.Provider value={data}>
      <h1>Nucleotide query</h1>
      <QueryBox />
    </SequenceContext.Provider>
  );
}

export default App;
