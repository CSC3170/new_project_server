import React, { useState } from 'react';
import { getLocalToken, setLocalToken } from '../api/Auth';
import { AuthContext } from './AuthContext';

const AuthProvider = ({ children }: { children: JSX.Element }) => {
  const [token, setStateToken] = useState(getLocalToken());

  const setToken = (newToken: string | null) => {
    setStateToken(newToken);
    setLocalToken(newToken);
  };

  return <AuthContext.Provider value={{ token, setToken }}>{children}</AuthContext.Provider>;
};

export { AuthProvider };
