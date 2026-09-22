import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { VittavaanApp } from "./App";
import "./styles.css";

const root = document.getElementById("root");
if (!root) throw new Error("Application root is missing");
createRoot(root).render(
  <StrictMode>
    <VittavaanApp />
  </StrictMode>,
);
