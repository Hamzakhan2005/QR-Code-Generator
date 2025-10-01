import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import "./components/QRCodeGenerator";
import QRCodeGenerator from "./components/QRCodeGenerator";
function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <QRCodeGenerator />
    </>
  );
}

export default App;
