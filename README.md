# 简历工作台 —— 免费部署指南（国内可访问版）

本部署包已为国内网络做适配：**不依赖任何被墙的外部资源**（无 Google Fonts、无境外 CDN，pdf.js 已本地化到 `vendor/`），部署后国内可直接访问。

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

## 🥇 推荐：腾讯云 EdgeOne Makers（Pages）—— 免备案 + 自定义域名 + 长期稳定

**先搞清规则（官方文档确认）：**

| 加速区域 | 免费默认域名 | 绑定自定义域名 |
|---------|------------|--------------|
| 中国大陆可用区 / 全球（含大陆） | 仅 3 小时预览链接，过期后大陆访问返回 **401** | **必须 ICP 备案** |
| **全球可用区（不含中国大陆）** | 3 小时预览链接 | **无需备案**，长期稳定 |

> 你之前的 401 就是「3 小时预览链接过期」导致的。长期访问的解法 = 加速区域选**不含中国大陆** + 绑定自定义域名，你的域名没备案也完全可以用。

**操作步骤：**

1. 打开 https://console.cloud.tencent.com/edgeone/pages （EdgeOne Makers，微信扫码登录腾讯云即可）
2. 创建项目 → 部署方式选 **上传静态资源 / Upload**：把 `index.html` 和 `vendor/` 一起上传（index.html 必须在根目录）；或用 GitHub 仓库 `over4edge/resume-workbench` 关联构建
3. **关键：加速区域选择「全球可用区（不含中国大陆）」**
4. 进入项目 → **域名管理** → 添加自定义域名 → 输入你的域名（如 `resume.example.com` 或 `example.com`）
5. 按弹窗指引，在域名注册商添加解析记录：
   - **归属验证记录**（TXT，弹窗会给出）
   - **CNAME 记录**：主机记录填子域名（如 `resume`），记录值填 Pages 提供的 `xxxx.xxx.dns.edgeone.site` 格式地址
6. 等待状态变为「已生效」（SSL 证书自动签发，无需手动申请），之后用 `https://你的域名` 长期访问

**注意：**

- 非中国大陆加速区域下，**大陆用户也能正常访问**（走海外边缘节点），速度中等但稳定免费；以后备案完成，可把区域切到含大陆以提速
- 域名 DNS 在境内注册商（阿里云 / 腾讯云 / 西部数码）均可直接添加 CNAME，**无需转移 DNS**
- 更新内容：项目里重新构建/上传即可，自定义域名始终指向最新部署
- 自定义域名可关联到「生产 / 预览」环境，测试和正式发布可分开

## 🥈 备用：腾讯云 CloudBase 静态托管（不用域名也能长期访问）

不想折腾域名时，CloudBase 静态托管的默认域名 `*.tcloudbaseapp.com` 国内可直接访问，**免费额度 1GB 存储 + 5GB/月流量，无备案、无 3 小时过期**；只有绑定自定义域名才要求备案。

1. 打开 https://console.cloud.tencent.com/tcb → 开通 CloudBase
2. 环境 → 静态网站托管 → 上传 `index.html` + `vendor/`
3. 得到 `https://xxx.tcloudbaseapp.com` 直接可用

## 🥉 海外备份：Cloudflare Pages / Netlify / GitHub Pages

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
