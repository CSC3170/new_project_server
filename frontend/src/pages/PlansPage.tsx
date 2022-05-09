import React from 'react';
import { RequireAuth } from '../auth/RequireAuth';
import { Plans } from '../components/Plans';

const PlansPage = () => {
  return (
    <RequireAuth>
      <div style={{ display: 'flex', height: '100%', justifyContent: 'center', alignItems: 'center' }}>
        <Plans />
      </div>
    </RequireAuth>
  );
};

export { PlansPage };
