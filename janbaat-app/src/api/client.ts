// Phase 7 — Axios instance + JWT interceptor
import axios from "axios";
import { supabase } from "./supabase";

export const apiClient = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT from Supabase session on every request
apiClient.interceptors.request.use(async (config) => {
  const {
    data: { session },
  } = await supabase.auth.getSession();
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
});

// Auto-refresh on 401
apiClient.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401) {
      const { data } = await supabase.auth.refreshSession();
      if (data.session) {
        error.config.headers.Authorization = `Bearer ${data.session.access_token}`;
        return apiClient.request(error.config);
      }
    }
    return Promise.reject(error);
  }
);
