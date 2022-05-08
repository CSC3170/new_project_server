interface Book {
  book_id: number;
  name: string;
  description: string | null;
  words_count: number;
}

export { type Book };
