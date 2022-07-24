import json
import logging, requests, pymysql, app
from bs4 import BeautifulSoup


def assert_utils(self, response, status_code, status, desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))


def request_third_api(form_data):
    # 解析form表单内容并提取请求参数
    soup = BeautifulSoup(form_data, 'html.parser')
    third_url = soup.form['action']
    logging.info("第三方URL：{}".format(third_url))
    data = {}  # 字典
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    response = requests.post(third_url, data=data)
    logging.info("第三方传输数据：{}".format(form_data))
    return response


class DBUtils:
    @classmethod
    def get_connect(cls, db_name):
        conn = pymysql.connect(app.DB_URL, app.DB_USERNAME, app.DB_PASSWORD, db_name, autocommit=True)
        return conn

    @classmethod
    def close(cls, cursor=None, conn=None):
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    @classmethod
    def delete(cls, db_name, sql):
        try:
            conn = cls.get_connect(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor, conn)


def read_img_verify_data(file_name):
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file, encoding='utf-8') as f:
        verify_data = json.load(f)
        test_data_list = verify_data.get("test_get_img_verify_code")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"), test_data.get("status_code")))
    print("json data：{}".format(test_case_data))
    return test_case_data


def read_register_data(file_name):
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file, encoding='utf-8') as f:
        register_data = json.load(f)
        test_data_list = register_data.get("test_register")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("phone"), test_data.get("pwd"), test_data.get("imgVerifyCode"),
                                   test_data.get("phoneCode"), test_data.get("dyServer"), test_data.get("invite_phone"),
                                   test_data.get("status_code"), test_data.get("status"), test_data.get("description")))
    print("json data：{}".format(test_case_data))
    return test_case_data

# 读取所有参数数据文件方法
def read_data(file_name, method_name, param_name):
    """

    :param file_name:  参数数据文件名
    :param method_name: 参数数据文件中定义的测试数据列表名
    :param param_name:  参数数据文件一组测试数据中所有参数组成的字符串
    :return:
    """
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file,encoding='utf-8') as f:
        file_data = json.load(f)
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
            # 不知道test_data有多少case；先把test_data对应的一组测试数据全部读取出来生成一个list
            test_params = []
            for param in param_name.split(','):
                # 依次获取同一组数据每个参数的值，添加到test_params形成一个list
                test_params.append(test_data.get(param))

            # 每完成一组测试数据的读取，就添加到test_case_data，直到所有测试数字读取完毕
            test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data



