import { Button, Card, Col, Form, Input, Row } from 'antd';
import React, { useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { login } from '../api/Auth';
import { AuthContext } from '../auth/AuthContext';
import { OAuth2PasswordRequestForm } from '../model/OAuth2PasswordRequestForm';

const Login = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);
  const [form] = Form.useForm();

  const onFinish = async (values: OAuth2PasswordRequestForm) => {
    await login(values, authContext);
    navigate('/', { state: { from: location } });
  };

  const onFinishFailed = () => {
    console.log('Failed');
  };

  const onReset = () => {
    form.resetFields();
  };

  return (
    <Card title='Login' style={{ width: 400 }}>
      <Form
        name='basic'
        labelCol={{ span: 6 }}
        wrapperCol={{ span: 16 }}
        initialValues={{ remember: true }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete='off'
      >
        <Form.Item
          label='Username'
          name='username'
          rules={[{ required: true, message: 'Please input your username!' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label='Password'
          name='password'
          rules={[{ required: true, message: 'Please input your password!' }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
          <Row justify='space-around'>
            <Col>
              <Button type='primary' htmlType='submit'>
                Submit
              </Button>
            </Col>
            <Col>
              <Button htmlType='button' onClick={onReset}>
                Reset
              </Button>
            </Col>
          </Row>
        </Form.Item>
      </Form>
    </Card>
  );
};

export { Login };
