import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import NewCall from "./pages/NewCall";
import History from "./pages/History";
import BoatStageDemo from "@/pages/BoatStageDemo";
import MotionPing from "./pages/MotionPing";
import Vessels from "./pages/Vessels";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/vessels" element={<Vessels />} />
          <Route path="/new-call" element={<NewCall />} />
          <Route path="/history" element={<History />} />
          <Route path="/demo/boats" element={<BoatStageDemo />} />
          <Route path="/ping" element={<MotionPing />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
