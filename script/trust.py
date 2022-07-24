from random import random
import unittest, logging, requests
from api.login_api import login_api
from api.trust_api import trustAPI
from utils import assert_utils, request_third_api


class trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = login_api()
        self.trust_api = trustAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 开户请求
    def test01_trust_request(self):
        # 1.登录
        response = self.login_api.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')

        # 2.发送开户请求
        response = self.trust_api.trust_register(self.session)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

        # 3.发送第三方开户请求
        form_data = response.json().get("description").get("form")
        # 解析form表单内容并提取请求参数
        response = request_third_api(form_data)
        # 断言
        self.assertEqual(200, response.status_code)
        self.assertEqual('UserRegister OK', response.text)

    # 充值成功
    def test02_recharge(self):
        # 1.登录
        response = self.login_api.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')
        # 2.获取充值验证码
        r = random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)

        # 3.发送充值请求
        response = self.trust_api.recharge(self.session,'10000')
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get('status'))
        # 4.发送第三方充值请求
        form_data = response.json().get("description").get("form") # 先提取表单数据
        response = request_third_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('NetSave OK', response.text)
