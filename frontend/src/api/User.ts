import { User } from '../model/User';

const queryUser = async () => {
  const res = await fetch('/api/user', {
    method: 'GET',
  });
  if (!res.ok) {
    throw new Error(res.statusText);
  }
  return (await res.json()) as User;
};

export { queryUser };
