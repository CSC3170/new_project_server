import _ from 'lodash';
import React, { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const RequireNotAuth = ({ children }: { children: JSX.Element }) => {
  const { token } = useContext(AuthContext);
  const location = useLocation();
  if (!_.isNull(token)) {
    return <Navigate to='/' state={{ from: location }} replace />;
  }
  return children;
};

export { RequireNotAuth };
