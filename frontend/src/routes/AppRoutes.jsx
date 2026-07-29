// frontend/src/routes/AppRoutes.jsx

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute";
import Layout from "../components/layout/Layout";
import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import Dashboard from "../pages/Dashboard";
import Studio from "../pages/Studio";
import useAuthStore from "../store/authStore";
import Compare from "../pages/Compare";
import Library from "../pages/Library";
import InferencePage from "../pages/InferencePage";
import VoiceQAPage from "../pages/VoiceQAPage";
import CNNPage from "../pages/CNNPage";

import History from "../pages/History";
import ExperimentDetail from "../pages/history/ExperimentDetail";
import ComparisonDetail from "../pages/history/ComparisonDetail";
import InferenceDetail from "../pages/history/InferenceDetail";

export default function AppRoutes() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />} />
        <Route path="/register" element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Register />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/studio" element={<Studio />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/library/:category" element={<Library />} />
            <Route path="/infer/:taskName" element={<InferencePage />} />
            <Route path="/infer/cnn_gender" element={<CNNPage />} />
            <Route path="/infer/voice_qa" element={<VoiceQAPage />} />
            <Route path="/infer/:taskName" element={<InferencePage />} />

            <Route path="/history" element={<History />} />
            <Route path="/history/experiment/:id" element={<ExperimentDetail />} />
            <Route path="/history/comparison/:id" element={<ComparisonDetail />} />
            <Route path="/history/inference/:id" element={<InferenceDetail />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} />
      </Routes>
    </BrowserRouter>
  );
}