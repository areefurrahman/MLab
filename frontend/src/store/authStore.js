// frontend/src/store/authStore.js

import { create } from "zustand";

const useAuthStore = create((set) => ({

  
  // ─── State ───────────────────────────────────────────────────────────────
  user: null,
  isAuthenticated: false,
  isInitialized: false,  // has the app checked localStorage yet?

  // ─── Actions ──────────────────────────────────────────────────────────────
  setUser: (user) =>
    set({
      user,
      isAuthenticated: !!user,
    }),

  login: (user, accessToken, refreshToken) => {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
    set({
      user,
      isAuthenticated: true,
    });
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({
      user: null,
      isAuthenticated: false,
    });
  },

  setInitialized: () => set({ isInitialized: true }),
}));

export default useAuthStore;