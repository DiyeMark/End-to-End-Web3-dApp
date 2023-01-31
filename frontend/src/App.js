import "./App.css";
import "antd/dist/antd.css";
import "./index.css";
import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Button, Checkbox, Form, Input } from "antd";
import TenAcademyLogo from "./10academy_logo.png";

function App() {
  const onFinish = (values) => {
    console.log("Received values of form: ", values);
  };
  return (
    <>
      <div className="flex flex-col min-h-screen">
        <div className=" w-48 p-8">
          <img src={TenAcademyLogo} alt="" />
        </div>
        <div className="grow flex flex-col justify-center items-center">
          <Form
            name="normal_login"
            className="w-1/5"
            initialValues={{
              remember: true,
            }}
            onFinish={onFinish}
          >
            <Form.Item
              name="email"
              rules={[
                {
                  required: true,
                  message: "Please input your email!",
                },
              ]}
            >
              <Input
                prefix={<MailOutlined className="site-form-item-icon" />}
                placeholder="Email"
              />
            </Form.Item>
            <Form.Item
              name="password"
              rules={[
                {
                  required: true,
                  message: "Please input your password!",
                },
              ]}
            >
              <Input
                prefix={<LockOutlined className="site-form-item-icon" />}
                type="password"
                placeholder="Password"
              />
            </Form.Item>
            <Form.Item>
              <Button type="danger" htmlType="submit" >
                <span className="hover:font-bold">
                  Log in
                </span>
              </Button>
            </Form.Item>
          </Form>
        </div>
      </div>
    </>
  );
}

export default App;
