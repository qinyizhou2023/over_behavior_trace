import "./App.css";

import { ExclamationTriangleIcon } from "@radix-ui/react-icons";

import { Editor } from "./components/lexical-editor";
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <main className="w-screen h-screen flex p-4">
      <Toaster closeButton={true} />
      {navigator.userAgent.indexOf("Chrome") === -1 ? (
        <Alert className="mx-auto my-auto w-100">
          <ExclamationTriangleIcon className="w-4 h-4" />
          <AlertTitle>Unsupported Browser</AlertTitle>
          <AlertDescription>
            Please use
            <a
              href="https://www.google.com/chrome/"
              target="_blank"
              rel="noreferrer"
              className="text-blue-500 px-1"
            >
              Chrome
            </a>
            to access WATOM console. Thanks for your understanding!
          </AlertDescription>
        </Alert>
      ) : (
        <Editor />
      )}
    </main>
  );
}

export default App;
