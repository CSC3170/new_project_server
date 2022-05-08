import { Button, Col, Form, Input, Row } from 'antd';
import React from 'react';

const Register = () => {
  const [form] = Form.useForm();

  const onFinish = () => {
    //
  };

  const onReset = () => {
    form.resetFields();
  };

  return (
    <Form
      name='basic'
      labelCol={{ span: 6 }}
      wrapperCol={{ span: 16 }}
      initialValues={{ remember: true }}
      onFinish={onFinish}
      // onFinishFailed={onFinishFailed}
      autoComplete='off'
      style={{ width: 400 }}
    >
      <Form.Item label='Username' name='name' rules={[{ required: true, message: 'Please input your username!' }]}>
        <Input />
      </Form.Item>

      <Form.Item label='Password' name='password' rules={[{ required: true, message: 'Please input your password!' }]}>
        <Input.Password />
      </Form.Item>

      <Form.Item label='Nickname' name='nickname'>
        <Input />
      </Form.Item>

      <Form.Item label='Email' name='email'>
        <Input />
      </Form.Item>

      <Form.Item label='Phone' name='phone'>
        <Input />
      </Form.Item>

      <Form.Item wrapperCol={{ offset: 6, span: 16 }}>
        <Row justify='space-around'>
          <Col>
            <Button type='primary' htmlType='submit' style={{ width: 100 }}>
              Login
            </Button>
          </Col>
          <Col>
            <Button htmlType='button' onClick={onReset} style={{ width: 100 }}>
              Reset
            </Button>
          </Col>
        </Row>
      </Form.Item>
    </Form>
  );
};

export { Register };
