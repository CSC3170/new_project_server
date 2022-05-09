import { createContext } from 'react';

interface AuthContextType {
  token: string | null;
  setToken: (newToken: string | null, rememberMe?: boolean) => void;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  setToken: () => {
    // do nothing;
  },
});

export { type AuthContextType, AuthContext };
