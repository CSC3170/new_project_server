import _ from 'lodash';
import { AuthContextType } from '../auth/AuthContext';
import { OAuth2PasswordRequestForm } from '../model/OAuth2PasswordRequestForm';

const getLocalToken = () => {
  return localStorage.getItem('token');
};

const setLocalToken = (token: string | null) => {
  if (_.isNull(token)) {
    localStorage.removeItem('token');
  } else {
    return localStorage.setItem('token', token);
  }
};

const login = async (form: OAuth2PasswordRequestForm, authContext: AuthContextType) => {
  const res = await fetch('/api/token', {
    method: 'POST',
    body: new URLSearchParams({
      username: form.username,
      password: form.password,
      grant_type: 'password',
    }),
  });
  if (!res.ok) {
    throw Error(res.statusText);
  }
  const tokenRes = (await res.json()) as {
    access_token: string;
    token_type: string;
  };
  const token = tokenRes.access_token;
  authContext.setToken(token);
  return token;
};

const logout = async (authContext: AuthContextType) => {
  authContext.setToken(null);
};

export { getLocalToken, login, logout, setLocalToken };
