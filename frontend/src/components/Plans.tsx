import { DoubleRightOutlined } from '@ant-design/icons';
import { Avatar, Col, Divider, Row } from 'antd';
import _ from 'lodash';
import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { queryBookById } from '../api/Book';
import { queryDailyPlans } from '../api/DailyPlan';
import { AuthContext } from '../auth/AuthContext';
import { IBook } from '../model/Book';
import { IDailyPlan } from '../model/DailyPlan';

interface PlanItemProps {
  bookName: string;
  bookWordsCount: number;
  progress: number;
}

const PlanItem = ({ bookName, bookWordsCount, progress }: PlanItemProps) => {
  const [hover, setHover] = useState(false);

  const onMouseEnter = () => {
    setHover(true);
  };

  const onMouseLeave = () => {
    setHover(false);
  };

  return (
    <Link to={`/daily-plan/${bookName}/word`}>
      <Row
        align='middle'
        gutter={16}
        style={{
          background: hover ? 'var(--item-hover-bg)' : 'none',
          paddingTop: '5%',
          paddingBottom: '5%',
        }}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
      >
        <Col flex='none'>
          <Avatar size={50} style={{ backgroundColor: '#22075e', verticalAlign: 'middle' }}>
            {bookName[0]}
          </Avatar>
        </Col>
        <Col flex='auto'>
          <Row>
            <Col style={{ lineHeight: '100%', fontSize: 20, color: 'var(--text-color)' }}>{bookName}</Col>
          </Row>
          <Row>
            <Col
              style={{ lineHeight: '100%', fontSize: 16, color: 'var(--text-color-secondary)' }}
            >{`${progress}/${bookWordsCount}`}</Col>
          </Row>
        </Col>
        <Col flex='none'>
          <DoubleRightOutlined style={{ color: 'var(--text-color)' }} />
        </Col>
      </Row>
    </Link>
  );
};

const Plans = () => {
  const authContext = useContext(AuthContext);

  const [dailyPlans, setDailyPlans] = useState<IDailyPlan[]>();
  const [books, setBooks] = useState<IBook[]>();

  useEffect(() => {
    (async () => {
      const newDailyPlans = await queryDailyPlans(authContext);
      const newBooks = await Promise.all(
        newDailyPlans.map(async (newDailyPlan) => {
          const newBook = await queryBookById(newDailyPlan.book_id, authContext);
          return newBook;
        }),
      );
      return [newDailyPlans, newBooks] as [IDailyPlan[], IBook[]];
    })().then(([newDailyPlans, newBooks]) => {
      setDailyPlans(newDailyPlans);
      setBooks(newBooks);
    });
  }, [authContext]);

  if (dailyPlans == null || books == null) {
    return <></>;
  }

  return (
    <div style={{ width: '80%', maxWidth: 300 }}>
      <Row justify='center'>
        <Col style={{ fontSize: 24, color: 'var(--text-secondary-color)' }}>Please select a book</Col>
      </Row>
      <Divider orientation='left' plain />
      {(_.zip(dailyPlans, books) as [IDailyPlan, IBook][]).map(([dailyPlan, book]) => {
        return (
          <PlanItem
            bookName={book.name}
            bookWordsCount={book.words_count}
            progress={dailyPlan.progress}
            key={book.book_id}
          />
        );
      })}
    </div>
  );
};

export { Plans };
