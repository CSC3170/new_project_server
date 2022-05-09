import React from 'react';
import { RequireNotAuth } from '../auth/RequireNotAuth';
import { Register } from '../components/Register';

const RegisterPage = () => {
  return (
    <RequireNotAuth>
      <div style={{ display: 'flex', height: '100%', justifyContent: 'center', alignItems: 'center' }}>
        <Register />
      </div>
    </RequireNotAuth>
  );
};

export { RegisterPage };
