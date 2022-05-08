import { CheckOutlined, CloseOutlined, DoubleRightOutlined } from '@ant-design/icons';
import { Button, Col, Row } from 'antd';
import React, { ComponentProps, useContext, useState } from 'react';
import { submitDailyPlanWord } from '../api/DailyPlan';
import { AuthContext } from '../auth/AuthContext';
import { WordType } from '../model/Word';

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
  return (
    <Button size='large' icon={<DoubleRightOutlined />} onClick={props.onClick}>
      NEXT
    </Button>
  );
};

interface WordPropsType {
  bookName: string;
  word: WordType;
  setRefreshing: (newRefreshing: boolean) => void;
}

const Word = ({ bookName, word, setRefreshing }: WordPropsType) => {
  const authContext = useContext(AuthContext);

  if (!word.is_submitted) {
    return (
      <Row align='middle' style={{ height: '100%' }}>
        <Col span={24}>
          <Row align='middle' justify='center'>
            <Col
              span={20}
              style={{
                textAlign: 'center',
              }}
            >
              <p
                style={{
                  fontSize: 48,
                  color: '#595959',
                }}
              >
                {word.spelling}
              </p>
            </Col>
          </Row>
          <Row align='middle' justify='center'>
            <Col>
              <p
                style={{
                  fontSize: 20,
                  color: '#595959',
                }}
              >
                Do you know the word?
              </p>
            </Col>
          </Row>
          <Row align='middle' justify='center' gutter={64}>
            <Col
              span={10}
              style={{
                textAlign: 'right',
              }}
            >
              <CheckMarkButton
                onClick={() => {
                  submitDailyPlanWord(bookName, authContext);
                  setRefreshing(true);
                }}
              />
            </Col>
            <Col
              span={10}
              style={{
                textAlign: 'left',
              }}
            >
              <XMarkButton
                onClick={() => {
                  submitDailyPlanWord(bookName, authContext);
                  setRefreshing(true);
                }}
              />
            </Col>
          </Row>
        </Col>
      </Row>
    );
  } else {
    return (
      <Row align='middle' style={{ height: '100%' }}>
        <Col span={24}>
          <Row align='middle' justify='center'>
            <Col
              span={20}
              style={{
                textAlign: 'center',
              }}
            >
              <p
                style={{
                  fontSize: 48,
                  color: '#595959',
                }}
              >
                {word.spelling}
              </p>
            </Col>
          </Row>
          <Row align='middle' justify='center'>
            <Col
              span={20}
              style={{
                textAlign: 'center',
              }}
            >
              <p
                style={{
                  fontSize: 30,
                  color: '#595959',
                }}
              >
                {word.translation}
              </p>
            </Col>
          </Row>
          <Row align='middle' justify='center'>
            <Col
              span={12}
              style={{
                textAlign: 'center',
              }}
            >
              <NextPageButton
                onClick={() => {
                  submitDailyPlanWord(bookName, authContext);
                  setRefreshing(true);
                }}
              />
            </Col>
          </Row>
        </Col>
      </Row>
    );
  }
};

export { Word };
