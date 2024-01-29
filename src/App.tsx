import "./App.css";

import { Editor } from "./components/lexical-editor";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <main className="w-screen h-screen flex p-4">
      <Toaster />
      <Editor />
    </main>
  );
}

export default App;
