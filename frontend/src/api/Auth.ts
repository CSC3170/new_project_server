import { AuthContextType } from '../auth/AuthContext';
import { OAuth2PasswordRequestForm } from '../model/OAuth2PasswordRequestForm';

const getLocalStorageToken = () => {
  return localStorage.getItem('token');
};

const setLocalStorageToken = (token: string) => {
  localStorage.setItem('token', token);
};

const removeLocalStorageToken = () => {
  localStorage.removeItem('token');
};

const login = async (form: OAuth2PasswordRequestForm, authContext: AuthContextType) => {
  const username = form.username;
  const password = form.password;
  const rememberMe = form.rememberMe;
  const res = await fetch('/api/token', {
    method: 'POST',
    body: new URLSearchParams({
      username: username,
      password: password,
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
  authContext.setToken(token, rememberMe);
  return token;
};

const logout = async (authContext: AuthContextType) => {
  authContext.setToken(null);
};

export { getLocalStorageToken, login, logout, removeLocalStorageToken, setLocalStorageToken };
