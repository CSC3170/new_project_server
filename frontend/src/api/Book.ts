import { AuthContextType } from '../auth/AuthContext';
import { Book } from '../model/Book';

const queryBookById = async (book_id: number, authContext: AuthContextType) => {
  const res = await fetch(`/api/book-by-id/${book_id}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authContext.token}`,
    },
  });
  if (!res.ok) {
    if (res.status == 400) {
      authContext.setToken(null);
    } else {
      throw new Error(res.statusText);
    }
  }
  return (await res.json()) as Book;
};

export { queryBookById };
