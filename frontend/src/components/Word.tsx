import { CheckOutlined, CloseOutlined, DoubleRightOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import React, { ComponentProps, useContext, useEffect, useState } from 'react';
import { queryDailyPlanWord, submitDailyPlanWord } from '../api/DailyPlan';
import { AuthContext } from '../auth/AuthContext';
import { IWord } from '../model/Word';

const CheckMarkButton = (props: ComponentProps<typeof Button>) => {
  const [hover, setHover] = useState(false);

  const onMouseEnter = () => {
    setHover(true);
  };

  const onMouseLeave = () => {
    setHover(false);
  };

  if (!hover) {
    return (
      <Button
        type='primary'
        danger
        ghost
        shape='circle'
        size='large'
        icon={<CheckOutlined />}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onClick={props.onClick}
      />
    );
  } else {
    return (
      <Button
        type='primary'
        danger
        shape='circle'
        size='large'
        icon={<CheckOutlined />}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onClick={props.onClick}
      />
    );
  }
};

const XMarkButton = (props: ComponentProps<typeof Button>) => {
  const [hover, setHover] = useState(false);

  const onMouseEnter = () => {
    setHover(true);
  };

  const onMouseLeave = () => {
    setHover(false);
  };

  if (!hover) {
    return (
      <Button
        type='primary'
        ghost
        shape='circle'
        size='large'
        icon={<CloseOutlined />}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onClick={props.onClick}
      />
    );
  } else {
    return (
      <Button
        type='primary'
        shape='circle'
        size='large'
        icon={<CloseOutlined />}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onClick={props.onClick}
      />
    );
  }
};

const NextPageButton = (props: ComponentProps<typeof Button>) => {
  const [hover, setHover] = useState(false);

  const onMouseEnter = () => {
    setHover(true);
  };

  const onMouseLeave = () => {
    setHover(false);
  };

  if (!hover) {
    return (
      <Button
        size='large'
        icon={<DoubleRightOutlined />}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onClick={props.onClick}
      >
        NEXT
      </Button>
    );
  } else {
    return (
      <Button
        type='primary'
        size='large'
        icon={<DoubleRightOutlined />}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onClick={props.onClick}
      >
        NEXT
      </Button>
    );
  }
};

interface WordItemProps {
  bookName: string;
  word: IWord;
  setRefreshing: (newRefreshing: boolean) => void;
}

const NotSubmittedWordItem = ({ bookName, word, setRefreshing }: WordItemProps) => {
  const authContext = useContext(AuthContext);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        width: '80%',
      }}
    >
      <p
        style={{
          fontSize: 48,
          color: 'var(--text-color)',
          wordBreak: 'break-all',
        }}
      >
        {word.spelling}
      </p>
      <p
        style={{
          fontSize: 20,
          color: 'var(--text-color-secondary)',
        }}
      >
        Do you know the word?
      </p>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          textAlign: 'center',
          width: '100%',
          maxWidth: 200,
        }}
      >
        <CheckMarkButton
          onClick={() => {
            submitDailyPlanWord(bookName, authContext);
            setRefreshing(true);
          }}
        />
        <XMarkButton
          onClick={() => {
            submitDailyPlanWord(bookName, authContext);
            setRefreshing(true);
          }}
        />
      </div>
    </div>
  );
};

const SubmittedWordItem = ({ bookName, word, setRefreshing }: WordItemProps) => {
  const authContext = useContext(AuthContext);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
      }}
    >
      <p
        style={{
          fontSize: 48,
          color: 'var(--text-color)',
          wordBreak: 'break-all',
          textAlign: 'center',
          width: '80%',
        }}
      >
        {word.spelling}
      </p>
      <p
        style={{
          fontSize: 36,
          color: 'var(--text-color)',
          wordBreak: 'break-all',
          textAlign: 'center',
          maxWidth: '80%',
        }}
      >
        {word.translation}
      </p>
      <NextPageButton
        onClick={() => {
          submitDailyPlanWord(bookName, authContext);
          setRefreshing(true);
        }}
      />
    </div>
  );
};

const Word = ({ bookName }: { bookName: string }) => {
  const authContext = useContext(AuthContext);
  const [refreshing, setRefreshing] = useState(false);
  const [word, setWord] = useState<IWord>();

  useEffect(() => {
    queryDailyPlanWord(bookName, authContext).then((newWord) => {
      setWord(newWord);
      setRefreshing(false);
    });
  }, [bookName, authContext, refreshing]);

  if (word == null) {
    return <></>;
  }

  if (!word.is_submitted) {
    return <NotSubmittedWordItem bookName={bookName} word={word} setRefreshing={setRefreshing} />;
  } else {
    return <SubmittedWordItem bookName={bookName} word={word} setRefreshing={setRefreshing} />;
  }
};

export { Word };
