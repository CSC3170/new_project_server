import React, { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { queryDailyPlanWord } from '../api/DailyPlan';
import { AuthContext } from '../auth/AuthContext';
import { RequireAuth } from '../auth/RequireAuth';
import { Word } from '../components/Word';
import { WordType } from '../model/Word';

const WordPage = () => {
  const { bookName } = useParams();
  const authContext = useContext(AuthContext);
  const [refreshing, setRefreshing] = useState(false);
  const [word, setWord] = useState<WordType>();

  useEffect(() => {
    queryDailyPlanWord(bookName as string, authContext).then((newWord) => {
      setWord(newWord);
      setRefreshing(false);
    });
  }, [bookName, authContext, refreshing]);

  if (bookName == null || word == null) {
    return (
      <RequireAuth>
        <></>
      </RequireAuth>
    );
  } else {
    return (
      <RequireAuth>
        <>
          <Word bookName={bookName} word={word} setRefreshing={setRefreshing} />
        </>
      </RequireAuth>
    );
  }
};

export { WordPage };
