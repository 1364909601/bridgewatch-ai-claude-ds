# BridgeWatch AI

基于现有 PRD 和要件说明实现的前端可演示版本，聚焦：

- 普通桥梁重大风险总览
- 长大桥梁船撞融合监测
- 隧道环境与异常预警
- 模型运行与推理任务看板

## 技术栈

- React 19
- Vite
- TypeScript
- Tailwind CSS v4
- Recharts
- Framer Motion
- `@google/genai`

## 启动

```bash
npm install
npm run dev
```

## AI 适配说明

- 默认不配置 API Key 时，页面右上角的 AI 运维简报使用本地 mock 逻辑生成。
- 如需接入 Gemini，在 `.env.local` 中配置：

```bash
VITE_GEMINI_API_KEY=your_key_here
VITE_GEMINI_MODEL=gemini-2.5-flash
```

- 当前是纯前端演示版，Gemini Key 会暴露在浏览器端环境变量中，只适合 Demo。正式环境应改为后端代理调用。

## 设计方向

- 采用硬件工具风格仪表盘
- 主色遵循需求文件中的 `#F0F0EE / #1A1A17`
- 使用 Inter、JetBrains Mono、Cormorant Garamond 形成展示、数据、标题的层级

## 参考

- Tailwind CSS 官方 Vite 集成：<https://tailwindcss.com/docs/installation/using-vite>
- Gemini JS SDK Quickstart：<https://ai.google.dev/gemini-api/docs/quickstart>
