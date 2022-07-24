import logging
import time
import unittest
import random

from parameterized import parameterized

from utils import assert_utils, read_img_verify_data
import requests
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

    # 获取图片验证码成功（随机小数）
    def test01_get_img_code_random_float(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)

    # 获取图片验证码成功（随机整数）
    def test02_get_img_code_random_int(self):
        # 定义参数
        r = random.randint(1000000, 900000000)
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)

    # 获取图片验证码失败（参数为空）
    def test03_get_img_code_param_is_null(self):
        # 调用接口类中接口
        response = self.login_api.getImgCode("", self.session)
        # 接收返回结果并断言
        self.assertEqual(404, response.status_code)

    # 获取图片验证码失败（参数为字母）
    def test04_get_img_code_random_char(self):
        # 定义参数
        r = random.sample("abcdefghijklmn", 10)
        rand = ''.join(r)
        logging.info(rand)  # list拼接
        # 调用接口类中接口
        response = self.login_api.getImgCode(rand, self.session)
        # 接收返回结果并断言
        self.assertEqual(400, response.status_code)

    # 获取短信验证码成功
    def test05_get_sms_code_success(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)

        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone01, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

    # 获取短信验证码失败（图片验证码错误）
    def test06_get_sms_code_wrong_img_code(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)

        error_code = '1234'
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone01, error_code)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码失败（图片验证码为空）
    def test07_get_sms_code_img_code_is_null(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)

        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone01, '')
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码失败（手机号为空）
    def test08_get_sms_code_phone_is_null(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)

        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, '', self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, None)

    # 获取短信验证码失败（未调用获取图片验证码接口）
    def test09_get_sms_code_no_img_verify(self):
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone01, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 注册成功（仅必填参数）
    def test10_register_success_param_must(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone01, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 调用接口类中注册接口
        response = self.login_api.register(self.session, self.phone01, self.pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "注册成功")

    # 注册成功（全部参数）
    def test11_register_success_param_all(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone02, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 调用接口类中注册接口
        response = self.login_api.register(self.session, self.phone02, self.pwd, invite_phone=self.phone01)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "注册成功")

    # 注册失败（手机号已存在）
    def test12_register_phone_is_exist(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone01, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 调用接口类中注册接口
        response = self.login_api.register(self.session, self.phone01, self.pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "手机已存在!")

    # 注册失败（密码为空）
    def test13_register_pwd_is_null(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone03, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 调用接口类中注册接口
        response = self.login_api.register(self.session, self.phone03, '')
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 注册失败（图片验证码错误）
    def test14_register_img_code_is_wrong(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone04, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 调用接口类中注册接口
        response = self.login_api.register(self.session, self.phone04, self.pwd, imgVerifyCode='1234')
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "验证码错误!")

    # 注册失败（短信验证码错误）
    def test15_register_sms_code_is_wrong(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone04, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 调用接口类中注册接口
        response = self.login_api.register(self.session, self.phone04, self.pwd, phoneCode='123456')
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "验证码错误")

    # 注册失败（未同意协议）
    def test16_register_disagree_protocol(self):
        # 定义参数
        r = random.random()
        # 调用接口类中接口
        response = self.login_api.getImgCode(str(r), self.session)
        # 接收返回结果并断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中发送验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone04, self.imgCode)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 调用接口类中注册接口
        response = self.login_api.register(self.session, self.phone04, self.pwd, dyServer='off')
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "请同意我们的条款")

    # 登录成功
    def test17_login_success(self):
        # 调用接口类中登录接口
        response = self.login_api.login(self.session, self.phone01, self.pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "登录成功")

    # 登录失败（用户名不存在）
    def test18_login_phone_is_not_exist(self):
        # 调用接口类中登录接口
        response = self.login_api.login(self.session, '00010000002', self.pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "用户不存在")

    # 登录失败（密码为空）
    def test19_login_pwd_is_null(self):
        # 调用接口类中登录接口
        response = self.login_api.login(self.session, self.phone01, '')
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 登录失败（密码错误）
    def test20_login_pwd_is_null(self):
        wrong_pwd = 'error'
        # 1.密码错误1次
        response = self.login_api.login(self.session, self.phone01, wrong_pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        # 2.密码错误2次
        response = self.login_api.login(self.session, self.phone01, wrong_pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

        # 3.密码错误3次锁定
        response = self.login_api.login(self.session, self.phone01, wrong_pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        # 4.输入正确密码锁定
        response = self.login_api.login(self.session, self.phone01, self.pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        # 5.60s后输入正确密码登录成功
        time.sleep(60)
        response = self.login_api.login(self.session, self.phone01, self.pwd)
        # 接收返回结果并断言
        assert_utils(self, response, 200, 200, "登录成功")
