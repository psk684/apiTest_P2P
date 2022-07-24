import unittest
import requests
from utils import assert_utils
from api.approve_api import approveAPI
from api.login_api import login_api


class approve(unittest.TestCase):
    realname = '张三'
    cardId = '330601199909191424'

    def setUp(self) -> None:
        self.login_api = login_api()
        self.approve_api = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 认证成功
    def test01_approve_success(self):
        # 登录
        response = self.login_api.login(self.session)
        assert_utils(self, response, 200, 200, "登录成功")

        # 调用接口类中接口
        response = self.approve_api.approve(self.session, self.realname, self.cardId)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, '提交成功!')

    # 认证失败（姓名为空）
    def test02_approve_realname_is_null(self):
        # 登录
        response = self.login_api.login(self.session)
        assert_utils(self, response, 200, 200, "登录成功")

        # 调用接口类中接口
        response = self.approve_api.approve(self.session, '', self.cardId)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, '姓名不能为空')

    # 认证失败（身份证号为空）
    def test03_approve_cardId_is_null(self):
        # 登录
        response = self.login_api.login(self.session)
        assert_utils(self, response, 200, 200, "登录成功")

        # 调用接口类中接口
        response = self.approve_api.approve(self.session, self.realname, '')
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, '身份证号不能为空')

    # 获取认证信息
    def test04_get_approve(self):
        # 登录
        response = self.login_api.login(self.session)
        assert_utils(self, response, 200, 200, "登录成功")

        # 调用接口类中接口
        response = self.approve_api.getApprove(self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
