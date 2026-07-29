// frontend/src/App.jsx

import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { authApi } from "./api/authApi";
import useAuthStore from "./store/authStore";
import AppRoutes from "./routes/AppRoutes";
import Spinner from "./components/ui/Spinner";

export default function App() {
  const { login, logout, setInitialized, isInitialized } = useAuthStore();
  const hasToken = !!localStorage.getItem("access_token");

  const { data, isSuccess, isError } = useQuery({
    queryKey: ["auth", "me"],
    queryFn: authApi.getMe,
    enabled: hasToken,
    retry: false,
  });

  useEffect(() => {
    if (!hasToken) {
      setInitialized();
      return;
    }
    if (isSuccess && data) {
      login(data, localStorage.getItem("access_token"), localStorage.getItem("refresh_token"));
      setInitialized();
    }
    if (isError) {
      logout();
      setInitialized();
    }
  }, [hasToken, isSuccess, isError, data]);

  if (!isInitialized) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Spinner size="lg" />
      </div>
    );
  }

  return <AppRoutes />;
}