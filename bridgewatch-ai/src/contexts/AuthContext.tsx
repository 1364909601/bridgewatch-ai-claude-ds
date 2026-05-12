import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { getMe, login as apiLogin, type CurrentUser } from "../lib/api";
import { getToken, setToken, clearToken, isAuthenticated } from "../lib/auth";

interface AuthState {
  user: CurrentUser | null;
  loading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isLoggedIn: boolean;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // On mount: check if token exists and validate it
  useEffect(() => {
    if (isAuthenticated()) {
      getMe()
        .then((u) => setUser(u))
        .catch(() => {
          clearToken();
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    setError(null);
    setLoading(true);
    try {
      const result = await apiLogin(username, password);
      setToken(result.access_token);
      setUser({
        user_id: result.user_id,
        username: result.username,
        display_name: result.display_name,
        role: result.role,
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "登录失败";
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    clearToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        login,
        logout,
        isLoggedIn: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
