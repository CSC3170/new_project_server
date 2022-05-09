import React, { useState } from 'react';
import { getLocalStorageToken, removeLocalStorageToken, setLocalStorageToken } from '../api/Auth';
import { AuthContext } from './AuthContext';

const AuthProvider = ({ children }: { children: JSX.Element }) => {
  const [token, setStateToken] = useState(getLocalStorageToken());

  const setToken = (newToken: string | null, rememberMe = false) => {
    removeLocalStorageToken();
    setStateToken(newToken);
    if (rememberMe && newToken != null) {
      setLocalStorageToken(newToken);
    }
  };

  return <AuthContext.Provider value={{ token, setToken }}>{children}</AuthContext.Provider>;
};

export { AuthProvider };
