import http.server
import socketserver
import json
from typing import Any
import hashlib
import base64
from dotenv import load_dotenv
import os
from feishu_token_manager import FeishuTokenManager
from feishu_send_message import FeishuMessenger
from google_generative_ai import GoogleGenerativeAI
from aes_cipher import AESCipher

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_POST(self):
        if self.path == '/card':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f"Server started at localhost:{post_data}")
            response = self.handle_card_action(post_data)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), "utf8"))

        if self.path == '/event':
            token = token_manager.get_token()
            print(f"{token}")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f"Server started at localhost:{post_data}")
            response = self.handle_event_action(post_data)
            if response:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response), "utf8"))
    
    def handle_card_action(self, data):
        # 解析 JSON 数据
        parsed_data = json.loads(data)
        # 提取 challenge 字段
        challenge = parsed_data.get('challenge', '')
        # 构造响应
        response = {"challenge": challenge}
        return response

    def handle_event_action(self, data):
        response = {}
        # 解析 JSON 数据
        parsed_data = json.loads(data)
        # 提取 encrypt 字段
        encrypt = parsed_data.get('encrypt', '')
        cipher = AESCipher(os.environ.get('ENCRYPT_KEY'))

        # 解析 JSON 数据
        parsed_data = json.loads(cipher.decrypt_string(encrypt))

        print(f"parsed_data:{parsed_data}")

        if parsed_data.get('challenge', ''):
            response = {"challenge": parsed_data.get('challenge', '')}
        else:
            # 解析 message_id
            event_type = parsed_data['header']['event_type']

            if event_type == 'im.message.receive_v1':
                # 解析 message_id
                message_id = parsed_data['event']['message']['message_id']

                # 检查 message_id 是否已经处理过
                if message_id in processed_message_ids:
                    print(f"消息已处理，message_id: {message_id}")
                    return

                content_text = json.loads(parsed_data['event']['message']['content'])['text']
                print("Message ID:", message_id)
                print("content_text:", content_text)

                api_key = os.environ.get('GOOGLE_API_KEY')  # Replace with your API key
                google_ai = GoogleGenerativeAI(api_key)
                prompt_parts = [content_text]
                response_text = google_ai.generate_content(prompt_parts)
                print(response_text)

                messenger = FeishuMessenger(token_manager.get_token())
                response = messenger.send_message(message_id, response_text)
                print(response)

                # 将 message_id 标记为已处理
                processed_message_ids.add(message_id)
                print(f"处理了新消息，message_id: {message_id}")
            elif event_type == 'im.message.message_read_v1':
                response = {}

        return response

PORT = 60501
processed_message_ids = set()

if __name__ == "__main__":
    load_dotenv()
    app_id = os.environ.get('APP_ID')
    app_secret = os.environ.get('APP_SECRET')
    token_manager = FeishuTokenManager(app_id, app_secret)
    with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
        print(f"Server started at localhost:{PORT}")
        httpd.serve_forever()
