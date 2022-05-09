import React from 'react';
import { RequireNotAuth } from '../auth/RequireNotAuth';
import { Login } from '../components/Login';

const LoginPage = () => {
  return (
    <RequireNotAuth>
      <div style={{ display: 'flex', height: '100%', justifyContent: 'center', alignItems: 'center' }}>
        <Login />
      </div>
    </RequireNotAuth>
  );
};

export { LoginPage };
