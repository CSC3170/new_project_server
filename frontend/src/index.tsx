import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Home } from './views/Home';
import { NotFound } from './views/NotFound';
import { Test } from './views/Test';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/test' element={<Test />} />
        <Route path='*' element={<NotFound />} />
      </Routes>
    </Router>
  </React.StrictMode>,
);
