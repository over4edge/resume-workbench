/**
 * 简历工作台 —— 免费 AI 远程代理（Cloudflare Worker，免费额度 10 万次/天）
 *
 * 部署方法（约 2 分钟，免费）：
 *   1. 打开 https://dash.cloudflare.com → Workers & Pages → 创建 Worker
 *   2. 把本文件全部内容粘贴进 Worker 代码，点「部署」
 *   3. 复制生成的 https://xxx.workers.dev 地址
 *   4. 打开你的简历工作台 → 右上角「设置」→「远程 AI 代理地址」粘贴该地址 → 保存
 *      （可选）在 Worker 设置 → 变量 里加 DEEPSEEK_API_KEY，页面端就不用填 Key
 */
export default {
  async fetch(request, env) {
    const CORS = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    };
    const json = (data, status) => new Response(data, { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS } });

    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (request.method !== 'POST') return json(JSON.stringify({ error: 'method not allowed' }), 405);

    const url = new URL(request.url);
    if (url.pathname !== '/ai/chat') return json(JSON.stringify({ error: 'not found' }), 404);

    let body;
    try { body = await request.json(); } catch (e) { return json(JSON.stringify({ error: 'bad json' }), 400); }

    const endpoint = String(body.endpoint || '').trim();
    if (!/^https:\/\//.test(endpoint) || !endpoint.endsWith('/chat/completions')) {
      return json(JSON.stringify({ error: 'endpoint 必须是 https://.../chat/completions' }), 400);
    }

    const key = String(body.apiKey || '').trim() || env.DEEPSEEK_API_KEY || '';
    if (!key) return json(JSON.stringify({ error: '未配置 API Key' }), 400);

    const payload = {
      model: body.model || 'deepseek-chat',
      messages: body.messages,
      temperature: body.temperature == null ? 0.6 : body.temperature
    };

    let upstream;
    try {
      upstream = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key },
        body: JSON.stringify(payload)
      });
    } catch (e) {
      return json(JSON.stringify({ error: 'upstream request failed: ' + e.message }), 502);
    }
    const text = await upstream.text();
    return json(text, upstream.status);
  }
};
