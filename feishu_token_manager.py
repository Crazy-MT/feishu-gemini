import http.client
import json
import time

class FeishuTokenManager:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = None
        self.expire_time = None

    def is_token_expired(self):
        # 如果没有 token 或者当前时间超过过期时间，返回 True
        if not self.token or time.time() >= self.expire_time:
            return True
        return False

    def get_token(self):
        if self.is_token_expired():
            self.request_token()
        return self.token

    def request_token(self):
        conn = http.client.HTTPSConnection("open.feishu.cn")
        payload = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })

        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/open-apis/auth/v3/tenant_access_token/internal", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response = json.loads(data.decode("utf-8"))

        if response['code'] == 0:
            self.token = response['tenant_access_token']
            # 设置 token 过期时间（当前时间 + expire - 一小段时间以防边界情况）
            self.expire_time = time.time() + response['expire'] - 60
        else:
            raise Exception(f"Failed to get token: {response}")