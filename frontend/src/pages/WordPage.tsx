import React from 'react';
import { useParams } from 'react-router-dom';
import { RequireAuth } from '../auth/RequireAuth';
import { Word } from '../components/Word';

const WordPage = () => {
  const { bookName } = useParams();

  if (bookName == null) {
    return (
      <RequireAuth>
        <></>
      </RequireAuth>
    );
  }

  return (
    <RequireAuth>
      <div style={{ display: 'flex', height: '100%', justifyContent: 'center', alignItems: 'center' }}>
        <Word bookName={bookName} />
      </div>
    </RequireAuth>
  );
};

export { WordPage };
