import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Checkbox, Col, Form, Input, Row } from 'antd';
import React, { useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { login } from '../api/Auth';
import { AuthContext } from '../auth/AuthContext';
import { OAuth2PasswordRequestForm } from '../model/OAuth2PasswordRequestForm';

const Login = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  const onFinish = async (form: OAuth2PasswordRequestForm) => {
    console.log(form);
    await login(form, authContext);
    navigate('/', { state: { from: location } });
  };

  return (
    <Form initialValues={{ rememberMe: true }} style={{ width: '80%', maxWidth: 300 }} onFinish={onFinish}>
      <Row>
        <Col span={24}>
          <Form.Item name='username' rules={[{ required: true, message: 'Please input your Username!' }]}>
            <Input addonBefore={<UserOutlined />} placeholder='Username' size='large' style={{ width: '100%' }} />
          </Form.Item>
        </Col>
      </Row>

      <Row>
        <Col span={24}>
          <Form.Item name='password' rules={[{ required: true, message: 'Please input your Password!' }]}>
            <Input.Password
              addonBefore={<LockOutlined />}
              placeholder='Password'
              size='large'
              style={{ width: '100%' }}
            />
          </Form.Item>
        </Col>
      </Row>

      <Row>
        <Col span={12} style={{ textAlign: 'left' }}>
          <Form.Item name='rememberMe' valuePropName='checked'>
            <Checkbox>Remember me</Checkbox>
          </Form.Item>
        </Col>

        <Col span={12} style={{ textAlign: 'right' }}>
          <Form.Item>
            <a href=''>Forgot password</a>
          </Form.Item>
        </Col>
      </Row>

      <Row>
        <Col span={24}>
          <Form.Item>
            <Button htmlType='submit' type='primary' size='large' style={{ width: '100%' }}>
              Login
            </Button>
          </Form.Item>
        </Col>
      </Row>
    </Form>
  );
};

export { Login };
