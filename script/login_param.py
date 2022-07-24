import logging
import time
import unittest
import random
from utils import assert_utils, read_img_verify_data, read_register_data, read_data
import requests
from parameterized import parameterized
from api.login_api import login_api


class login(unittest.TestCase):
    phone01 = '13100001111'
    phone02 = '13100001112'
    phone03 = '13100001113'
    phone04 = '13100001114'
    pwd = '123456'
    imgCode = '8888'
    smsCode = '666666'

    def setUp(self) -> None:
        self.login_api = login_api()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 获取图片验证码（参数化）
    @parameterized.expand(read_img_verify_data("imgVerify.json"))
    def test01_get_img_code(self, types, status_code):
        # 根据不同type准备不同参数数据
        r = ''
        if types == 'float':
            r = str(random.random())
        elif types == 'int':
            r = str(random.randint(1000000, 90000000))
        elif types == 'char':
            r = ''.join(random.sample("abcdefghijklmn", 10))

        # 调用接口类中接口
        response = self.login_api.getImgCode(r, self.session)
        # 接收返回结果并断言
        self.assertEqual(status_code, response.status_code)

    # 注册（参数化）
    # @parameterized.expand(read_register_data("register.json"))
    @parameterized.expand(read_data("register.json", "test_register",
                                    "phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description"))
    def test02_register(self, phone, pwd, imgVerifyCode, phoneCode, dyServer, invite_phone, status_code, status,
                        description):
        # 1.获取图片&短信验证码成功
        r = random.random()
        response = self.login_api.getImgCode(str(r), self.session)
        self.assertEqual(200, response.status_code)
        response = self.login_api.getSmsCode(self.session, phone, self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 2.参数化测试数据注册并返回结果
        response = self.login_api.register(self.session, phone, pwd, imgVerifyCode, phoneCode, dyServer, invite_phone)
        logging.info("register响应：{}".format(response.json()))
        # 接收返回结果并断言
        assert_utils(self, response, status_code, status, description)

    # 获取图片验证码（参数化）
    @parameterized.expand(read_data("imgVerify.json", "test_get_img_verify_code", "type,status_code"))
    def test03_get_img_code(self, types, status_code):
        # 根据不同type准备不同参数数据
        r = ''
        if types == 'float':
            r = str(random.random())
        elif types == 'int':
            r = str(random.randint(1000000, 90000000))
        elif types == 'char':
            r = ''.join(random.sample("abcdefghijklmn", 10))

        # 调用接口类中接口
        response = self.login_api.getImgCode(r, self.session)
        # 接收返回结果并断言
        self.assertEqual(status_code, response.status_code)
