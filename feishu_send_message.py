import http.client
import json

class FeishuMessenger:
    def __init__(self, token):
        self.conn = http.client.HTTPSConnection("open.feishu.cn")
        self.token = token

    def send_message(self, message_id, message, uuid=""):
        payload = json.dumps({
            "content": json.dumps({"text": message}),
            "msg_type": "text",
            # "uuid": uuid
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        endpoint = f"/open-apis/im/v1/messages/{message_id}/reply"
        self.conn.request("POST", endpoint, payload, headers)
        res = self.conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

# Usage example:
# messenger = FeishuMessenger('your-access-token-here')
# response = messenger.send_message('message-id-here', 'Hello, this is a test message')
# print(response)
