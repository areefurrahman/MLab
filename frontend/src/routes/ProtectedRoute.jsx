// frontend/src/routes/ProtectedRoute.jsx

import { Navigate, Outlet } from "react-router-dom";
import useAuthStore from "../store/authStore";

export default function ProtectedRoute() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  // If not authenticated, redirect to login
  // Outlet renders the child route if authenticated
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}