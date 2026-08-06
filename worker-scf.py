# -*- coding: utf-8 -*-
"""
简历工作台 —— 国内免费 AI 远程代理（腾讯云云函数 SCF）

部署步骤（约 5 分钟，免费额度 40 万次/月）：
  1. 打开 https://console.cloud.tencent.com/scf → 函数服务 → 新建 → 从头开始
  2. 运行环境选 Python 3.6+，本文件内容粘贴进「在线编辑」→ 部署
  3. 触发方式：添加「API 网关触发器」→ 路径 /ai/chat → 请求方法 POST → 启用【集成响应】
  4. 部署后得到访问地址 https://xxxx.apigw.tencentcs.com/ai/chat
  5. 简历工作台网页版右上角「设置 → 远程 AI 代理地址」填 https://xxxx.apigw.tencentcs.com → 保存
  （若在函数环境变量里配 DEEPSEEK_API_KEY，页面端就不用填 Key）

注意：请确保 API 网关触发器的「集成响应」已开启，否则返回格式会被包装。
"""
import json
import os
import urllib.request
import urllib.error

def _resp(status, obj):
    body = json.dumps(obj, ensure_ascii=False)
    return {
        "isBase64Encoded": False,
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": body
    }

def main_handler(event, context):
    method = (event.get("httpMethod") or "POST").upper()
    if method == "OPTIONS":
        return _resp(200, {})
    body = event.get("body") or ""
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            return _resp(400, {"error": "bad json"})
    endpoint = str(body.get("endpoint") or "").strip()
    if not (endpoint.startswith("https://") and endpoint.endswith("/chat/completions")):
        return _resp(400, {"error": "endpoint 必须是 https://.../chat/completions"})
    api_key = str(body.get("apiKey") or "").strip() or os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return _resp(400, {"error": "未配置 API Key"})
    payload = {
        "model": body.get("model") or "deepseek-chat",
        "messages": body.get("messages") or [],
        "temperature": body.get("temperature", 0.6)
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            text = r.read().decode("utf-8", "replace")
        return _resp(r.status, json.loads(text))
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            err = {"error": "upstream http " + str(e.code)}
        return _resp(e.code, err)
    except Exception as e:
        return _resp(502, {"error": "upstream request failed: " + str(e)})
