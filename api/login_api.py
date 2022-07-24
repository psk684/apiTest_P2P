import app


class login_api():
    def __init__(self):
        self.getImgCode_url = app.BASE_URL + '/common/public/verifycode1/'
        self.getSmsCode_url = app.BASE_URL + '/member/public/sendSms'
        self.register_url = app.BASE_URL + '/member/public/reg'
        self.login_url = app.BASE_URL + '/member/public/login'

    # 获取图片验证码接口
    def getImgCode(self, r, session):
        url = self.getImgCode_url + r
        response = session.get(url)
        return response

    # 获取短信验证码接口
    def getSmsCode(self, session, phone, imgVerifyCode):
        data = {'phone': phone, 'imgVerifyCode': imgVerifyCode, 'type': 'reg'}
        response = session.post(self.getSmsCode_url, data=data)
        return response

    # 获取注册接口
    def register(self, session, phone, pwd, imgVerifyCode='8888', phoneCode='666666', dyServer='on', invite_phone=''):
        data = {'phone': phone, 'password': pwd, 'verifycode': imgVerifyCode, 'phone_code': phoneCode,
                'dy_server': dyServer, 'invite_phone': invite_phone}
        response = session.post(self.register_url, data=data)
        return response

    # 获取登录接口
    def login(self, session, phone='13100001111', pwd='123456'):
        data = {'keywords': phone, 'password': pwd}
        response = session.post(self.login_url, data=data)
        return response
