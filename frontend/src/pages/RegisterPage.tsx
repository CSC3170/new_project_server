import React from 'react';
import { RequireNotAuth } from '../auth/RequireNotAuth';
import { Register } from '../components/Register';

const RegisterPage = () => {
  return (
    <RequireNotAuth>
      <Register />
    </RequireNotAuth>
  );
};

export { RegisterPage };
