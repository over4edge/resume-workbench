# 简历工作台 —— 免费部署指南（国内可访问版）

本部署包已为国内网络做适配：**不依赖任何被墙的外部资源**（无 Google Fonts、无境外 CDN，pdf.js 已本地化到 `vendor/`），部署后国内直接秒开。

```
deploy/
├── index.html            # 应用本体（单文件，全部功能内嵌）
├── vendor/
│   ├── pdf.min.mjs       # AI 导入 PDF 解析（本地化，不走境外 CDN）
│   └── pdf.worker.min.mjs
├── worker-scf.py         # 国内免费 AI 代理（腾讯云云函数 SCF）
├── worker-proxy.js       # 海外免费 AI 代理（Cloudflare Worker，备用）
└── README.md
```

## 🥇 方式一（推荐）：腾讯云 EdgeOne Pages —— 国内秒开、免费、无需备案

EdgeOne Pages 是腾讯云的免费静态托管（公测免费），国内访问快，静态页面无需 ICP 备案。

1. 打开 https://console.cloud.tencent.com/edgeone/pages （用微信/QQ 登录腾讯云即可，新用户送免费额度）
2. 点「创建项目 / Create Project」→ 选 **上传静态资源 / Upload**
3. 把 `index.html` 和 `vendor/` 文件夹一起上传（保持 index.html 在根目录）
4. 部署完成后得到一个 `https://xxxx.edgeone.app` 网址，国内直接访问，发给谁都能用

> 如果没有腾讯云账号：微信扫码登录即可，实名认证是腾讯云对国内用户的通用要求（免费）。

## 🥈 方式二：Gitee Pages（国内备用）

1. 登录 https://gitee.com → 新建公开仓库
2. 上传 `index.html` 和 `vendor/` 到仓库根目录
3. 仓库 → 服务 → Gitee Pages → 部署（需先完成实名认证）
4. 得到 `https://用户名.gitee.io/仓库名/`

> 注意：Gitee Pages 需要实名认证，且更新后需手动重新部署；若该服务在你所在地区不可用，优先用方式一。

## 🥉 方式三（海外用户可选）：Netlify / GitHub Pages / Cloudflare Pages

国内访问不稳定，仅作海外备份：把 `index.html` 和 `vendor/` 拖到 https://app.netlify.com/drop 即可。

---

## 让 AI 功能在网页版也能用（国内免费代理）

静态托管跑不了 server.py，DeepSeek 又禁止浏览器直连，所以需要一个国内可访问的免费小代理。**推荐腾讯云云函数 SCF**（免费额度 40 万次/月，国内访问正常）：

1. 打开 https://console.cloud.tencent.com/scf → 新建函数 → 运行环境 Python 3.6+
2. 把 `worker-scf.py` 内容粘贴进在线编辑 → 部署
3. 添加「API 网关触发器」：路径 `/ai/chat`、方法 POST、**开启【集成响应】**
4. 复制得到的 `https://xxxx.apigw.tencentcs.com` 地址
5. 打开你的网页版简历工作台 → 右上角「设置」→「远程 AI 代理地址」粘贴该地址 → 保存
6. 可选：函数「环境变量」加 `DEEPSEEK_API_KEY` = 你的 Key，页面端就不用填 Key

> Cloudflare Worker（`worker-proxy.js`）在国内访问不稳定，仅作海外备用。

## 功能对照

| 功能 | 纯静态网页 | + 远程 AI 代理(SCF) |
|------|-----------|--------------------|
| 编辑 / 模板 / 配色 / 证件照 / 自动排版 | ✅ | ✅ |
| 导出 PDF / 图片 PNG | ✅ | ✅ |
| AI 导入旧简历 / AI 润色 | ❌ | ✅ |
| 导出 Word | ❌（本地 server.py 可导） | ❌ |
| 生僻字 PDF 不丢字 | 常用字内嵌（生僻字有提示） | 同左（完整保障仍需本地 server.py） |

## 隐私提示

- 纯静态版：数据只存在访问者自己的浏览器 localStorage，不上传任何服务器。
- 远程代理版：AI 请求经腾讯云函数转发给 DeepSeek；Key 建议放函数环境变量。

---

## 参考与致谢

本工具借鉴 / 参考了以下项目与资源：

| 来源 | 用途说明 |
|------|---------|
| [ruanyf/weekly#9104](https://github.com/ruanyf/weekly/issues/9104) | 最初的产品灵感（单文件简历制作工具） |
| [Viktor Oddy 官网](https://halaskastudio.com/) | 首页落地页视觉风格参考（白底、衬线大字标题、深色胶囊按钮、跑马灯与视差动效） |
| [pdf.js](https://github.com/mozilla/pdf.js) | AI 导入旧简历 PDF 的文字提取（v5.6.205，已本地化到 vendor/） |
| Hiragino Mincho ProN（macOS 系统字体） | 首页衬线强调字体的内嵌子集来源 |
