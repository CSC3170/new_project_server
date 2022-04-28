import React, { useEffect, useState } from 'react';
import { test } from '../http/test';

interface TestProps {
  id: number;
}

const TestImpl = ({ id }: TestProps) => {
  const [state, setState] = useState({
    data: '',
  });
  useEffect(() => {
    test(id).then((newState) => {
      setState(newState);
    });
  }, [id]);
  return <h1>hello, {state.data}</h1>;
};

const Test = () => {
  return <TestImpl id={1024} />;
};

export { Test };
