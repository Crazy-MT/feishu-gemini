# 项目名称
飞书机器人与谷歌 gemini-pro 集成应用
接入参考：[接入Gemini pro – 将Gemini pro集成到飞书机器人，直接拉满效率 - 掘金 (juejin.cn)](https://juejin.cn/post/7314605176832262171)

## 简介
这个项目是一个 Python 应用，旨在实现飞书机器人与谷歌生成型 AI 的集成。用户可以通过飞书客户端向机器人发送消息，机器人则通过该应用访问谷歌 AI 服务，实现智能回复和其他 AI 功能。

## 安装
克隆这个仓库到你的本地机器上：
```
git clone git@github.com:Crazy-MT/feishu-gemini.git
```

安装所需依赖：
```
pip install -r requirements.txt
```

## 配置
创建一个 `.env` 文件，并填写必要的环境变量：
```
# .env 文件内容
GOOGLE_API_KEY=google generative ai api key
APP_ID=飞书机器人 app_id
APP_SECRET=飞书机器人 app_secret
ENCRYPT_KEY=飞书机器人事件订阅的 Encrypt Key
```

## 使用
运行该命令将会监听 60501 端口，可以将服务器地址作为飞书机器人的事件订阅请求地址。
```
python3 feishu_gemini.py
```