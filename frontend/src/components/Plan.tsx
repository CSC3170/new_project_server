import 'antd/dist/antd.less';
import { DoubleRightOutlined } from '@ant-design/icons';
import { Avatar, Col, Divider, Row, Space } from 'antd';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

interface PlanPropsType {
  bookName: string;
  bookWordsCount: number;
  progress: number;
}

const Plan = ({ bookName, bookWordsCount, progress }: PlanPropsType) => {
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
        justify='center'
        gutter={[16, 24]}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        style={{
          backgroundColor: hover ? '#f0f0f0' : '#ffffff',
        }}
      >
        <Col
          span={5}
          style={{
            textAlign: 'right',
          }}
        >
          <Avatar
            size={50}
            style={{
              backgroundColor: '#22075e',
              verticalAlign: 'middle',
            }}
          >
            {bookName[0]}
          </Avatar>
        </Col>
        <Col
          span={10}
          style={{
            textAlign: 'left',
          }}
        >
          <Space direction='vertical'>
            <p
              style={{
                fontSize: 20,
                color: '#595959',
                lineHeight: 0,
              }}
            >
              {bookName}
            </p>
            <p
              style={{
                fontSize: 16,
                color: '#8c8c8c',
                lineHeight: 0,
              }}
            >
              {`${progress}/${bookWordsCount}`}
            </p>
          </Space>
        </Col>
        <Col
          span={5}
          style={{
            textAlign: 'right',
          }}
        >
          <DoubleRightOutlined
            style={{
              color: '#595959',
            }}
          />
        </Col>
      </Row>
      <Divider orientation='left' />
    </Link>
  );
};

export { Plan };
