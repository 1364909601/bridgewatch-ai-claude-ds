import type { DigestRequest, OperationsDigest } from "../types";

function makeMockDigest(request: DigestRequest): OperationsDigest {
  const selected = request.selectedEvent;
  const headline = selected
    ? `${request.pageTitle}：${selected.objectName} 已进入重点复核窗口`
    : `${request.pageTitle}：当前页面适合值守演示与态势汇报`;

  const bullets = [
    request.highlights[0] ?? "当前没有额外高亮信息。",
    selected
      ? `当前重点事件为“${selected.type}”，置信度 ${selected.confidence}%，触发信号为：${selected.sensorSignal}。`
      : request.highlights[1] ?? "核心信号保持稳定。",
    request.highlights[2] ?? "建议保留当前页面用于演示。"
  ];

  return {
    headline,
    bullets,
    source: "mock",
    generatedAt: new Date().toLocaleTimeString("zh-CN", { hour12: false })
  };
}

export async function generateOperationsDigest(
  request: DigestRequest
): Promise<OperationsDigest> {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  const model = import.meta.env.VITE_GEMINI_MODEL || "gemini-2.5-flash";

  if (!apiKey) {
    return makeMockDigest(request);
  }

  const prompt = [
    "你是桥梁与隧道监测中心的值守 AI 助理。",
    "请基于以下上下文，输出一条 22 字以内的中文 headline，以及 3 条简洁 bullet。",
    "只关注风险态势、复核动作、演示价值，不要写空话。",
    `页面：${request.pageTitle}`,
    `目标：${request.pageObjective}`,
    `高亮：${request.highlights.join("；")}`,
    request.selectedEvent
      ? `当前事件：${request.selectedEvent.objectName} / ${request.selectedEvent.type} / ${request.selectedEvent.riskLevel}风险 / 置信度 ${request.selectedEvent.confidence}% / ${request.selectedEvent.sensorSignal}`
      : "当前没有指定事件。",
    "输出格式：第一行以 HEADLINE: 开头，后续三行以 - 开头。"
  ].join("\n");

  try {
    const { GoogleGenAI } = await import("@google/genai");
    const ai = new GoogleGenAI({ apiKey });
    const response = await ai.models.generateContent({
      model,
      contents: prompt,
      config: {
        thinkingConfig: {
          thinkingBudget: 0
        }
      }
    });

    const text = response.text?.trim();
    if (!text) {
      return {
        ...makeMockDigest(request),
        source: "fallback"
      };
    }

    const lines = text
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    const fallback = makeMockDigest(request);
    const headlineLine = lines.find((line) => line.startsWith("HEADLINE:"));
    const bullets = lines
      .filter((line) => line.startsWith("-"))
      .map((line) => line.replace(/^-+\s*/, ""))
      .slice(0, 3);

    return {
      headline: headlineLine?.replace("HEADLINE:", "").trim() || fallback.headline,
      bullets: bullets.length > 0 ? bullets : fallback.bullets,
      source: "gemini",
      generatedAt: new Date().toLocaleTimeString("zh-CN", { hour12: false })
    };
  } catch {
    return {
      ...makeMockDigest(request),
      source: "fallback"
    };
  }
}
