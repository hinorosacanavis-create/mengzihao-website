import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域，方便前端 chat.html 直接调用

# 您的火山方舟 API Key
API_KEY = "ark-ec45d19d-2292-40e1-877d-b38edc88dabe-53377"

@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    prompt_text = data.get('prompt', '')
    base64_image = data.get('image', '')
    
    print(f"收到生图请求! Prompt: {prompt_text}")
    if base64_image:
        print("已附带参考图 base64 编码。")
    
    # 构造发送给火山方舟的请求
    # 注意：这里的 URL 和 payload 格式是通用的 OpenAI 格式。
    # 不同的图生图模型可能有独特的参数名（如 reference_image），请根据火山方舟的文档微调。
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        # 【重要】必须要填写 ep- 开头的接入点 ID 才能生图！
        "model": "ep-20260515202120-8rnrw", 
        "prompt": prompt_text,
        "n": 1,
        "response_format": "url" # 让大模型返回一个图片的 URL
    }
    
    # 如果有参考图，添加到请求里
    if base64_image:
        payload["image"] = base64_image

    try:
        print("正在调用火山方舟大模型...")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        print("大模型返回成功!")
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if e.response is not None:
            error_msg += f" | 响应详情: {e.response.text}"
        print("API 调用报错:", error_msg)
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    print("---------------------------------------")
    print("🚀 本地生图代理服务器已启动!")
    print("👉 监听地址: http://127.0.0.1:5001")
    print("---------------------------------------")
    app.run(port=5001, debug=True)
