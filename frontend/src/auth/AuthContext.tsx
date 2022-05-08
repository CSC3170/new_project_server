import { createContext } from 'react';

interface AuthContextType {
  token: string | null;
  setToken: (newToken: string | null) => void;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  setToken: () => {
    // do nothing;
  },
});

export { type AuthContextType, AuthContext };
