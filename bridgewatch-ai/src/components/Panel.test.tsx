import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Panel } from "./Panel";

describe("Panel", () => {
  it("renders title", () => {
    render(<Panel title="测试面板">内容</Panel>);
    expect(screen.getByText("测试面板")).toBeInTheDocument();
  });

  it("renders eyebrow text", () => {
    render(<Panel title="面板" eyebrow="Test Panel">内容</Panel>);
    expect(screen.getByText("Test Panel")).toBeInTheDocument();
  });

  it("renders children content", () => {
    render(<Panel title="面板"><span>子元素</span></Panel>);
    expect(screen.getByText("子元素")).toBeInTheDocument();
  });

  it("renders action element when provided", () => {
    render(<Panel title="面板" action={<button>操作</button>}>内容</Panel>);
    expect(screen.getByText("操作")).toBeInTheDocument();
  });
});
