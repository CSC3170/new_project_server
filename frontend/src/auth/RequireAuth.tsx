import React, { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const RequireAuth = ({ children }: { children: JSX.Element }) => {
  const { token } = useContext(AuthContext);
  const location = useLocation();
  if (token == null) {
    return <Navigate to='/login' state={{ from: location }} />;
  }
  return children;
};

export { RequireAuth };
