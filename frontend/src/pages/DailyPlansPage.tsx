import { Col, Divider, Row } from 'antd';
import _ from 'lodash';
import React, { useContext, useEffect, useState } from 'react';
import { queryBookById } from '../api/Book';
import { queryDailyPlans } from '../api/DailyPlan';
import { AuthContext } from '../auth/AuthContext';
import { RequireAuth } from '../auth/RequireAuth';
import { Plan } from '../components/Plan';
import { Book } from '../model/Book';
import { DailyPlan } from '../model/DailyPlan';

const DailyPlansPage = () => {
  const authContext = useContext(AuthContext);
  const [dailyPlans, setDailyPlans] = useState([] as DailyPlan[]);
  const [books, setBooks] = useState([] as Book[]);

  useEffect(() => {
    (async () => {
      const newDailyPlans = await queryDailyPlans(authContext);
      const newBooks = await Promise.all(
        newDailyPlans.map(async (newDailyPlan) => {
          const newBook = await queryBookById(newDailyPlan.book_id, authContext);
          return newBook;
        }),
      );
      return [newDailyPlans, newBooks] as [DailyPlan[], Book[]];
    })().then(([newDailyPlans, newBooks]) => {
      setDailyPlans(newDailyPlans);
      setBooks(newBooks);
    });
  }, [authContext]);

  return (
    <RequireAuth>
      <Row align='middle' style={{ height: '100%' }}>
        <Col span={24}>
          <Row align='middle' justify='center' gutter={[16, 24]}>
            <Col
              span={24}
              style={{
                textAlign: 'center',
              }}
            >
              <p
                style={{
                  fontSize: 24,
                  color: '#595959',
                }}
              >
                Please select a book
              </p>
            </Col>
          </Row>
          <Divider orientation='left' />
          {(_.zip(dailyPlans, books) as [DailyPlan, Book][]).map(([dailyPlan, book]) => {
            return (
              <Plan
                bookName={book.name}
                bookWordsCount={book.words_count}
                progress={dailyPlan.progress}
                key={dailyPlan.book_id}
              />
            );
          })}
        </Col>
      </Row>
    </RequireAuth>
  );
};

export { DailyPlansPage };
