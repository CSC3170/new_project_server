import React from 'react';
import { RequireNotAuth } from '../auth/RequireNotAuth';
import { Login } from '../components/Login';

const LoginPage = () => {
  return (
    <RequireNotAuth>
      <Login />
    </RequireNotAuth>
  );
};

export { LoginPage };
