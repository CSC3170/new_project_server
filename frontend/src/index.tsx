import 'antd/dist/antd.less';
import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './auth/AuthProvider';
import { DailyPlansPage } from './pages/DailyPlansPage';
import { LoginPage } from './pages/LoginPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { RegisterPage } from './pages/RegisterPage';
import { WordPage } from './pages/WordPage';

const root = createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <StrictMode>
    <AuthProvider>
      <Router>
        <Routes>
          <Route path='/' element={<DailyPlansPage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/register' element={<RegisterPage />} />
          <Route path='/daily-plan/:bookName/word' element={<WordPage />} />
          <Route path='*' element={<NotFoundPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  </StrictMode>,
);
