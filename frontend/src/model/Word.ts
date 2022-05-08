interface WordType {
  is_submitted: boolean;
  book_id: number;
  word_id: number;
  spelling: string;
  translation: string | null;
}

export { type WordType };
