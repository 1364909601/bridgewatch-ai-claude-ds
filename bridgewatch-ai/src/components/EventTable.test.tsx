import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { EventTable } from "./EventTable";
import type { EventRecord } from "../types";

const mockEvents: EventRecord[] = [
  {
    id: "EV-001", objectName: "南京长江大桥", objectType: "长大桥梁",
    title: "桥体坍塌风险", type: "collapse", riskLevel: "高", confidence: 97,
    scene: "白天", time: "14:31:45", camera: "UAV-03",
    clipRange: "02:11 - 02:28", status: "待复核",
    sensorSignal: "结构异常", description: "桥面突变",
    overlays: [{ id: "o1", label: "异常", left: 37, top: 42, width: 24, height: 14 }],
  },
  {
    id: "EV-002", objectName: "杭州湾大桥", objectType: "普通桥梁",
    title: "桥面变形", type: "deformation", riskLevel: "中", confidence: 85,
    scene: "雨雾", time: "14:30:22", camera: "UAV-08",
    clipRange: "01:06 - 01:24", status: "待复核",
    sensorSignal: "轮廓偏移", description: "连续帧异常",
    overlays: [{ id: "o2", label: "变形段", left: 29, top: 48, width: 31, height: 11 }],
  },
];

describe("EventTable", () => {
  it("renders table headers", () => {
    render(<EventTable events={[]} selectedEventId="" onSelect={() => {}} onPlayback={() => {}} />);
    expect(screen.getByText("时间")).toBeInTheDocument();
    expect(screen.getByText("事件")).toBeInTheDocument();
    expect(screen.getByText("风险")).toBeInTheDocument();
    expect(screen.getByText("场景")).toBeInTheDocument();
  });

  it("renders event rows", () => {
    render(<EventTable events={mockEvents} selectedEventId="" onSelect={() => {}} onPlayback={() => {}} />);
    expect(screen.getByText("桥体坍塌风险")).toBeInTheDocument();
    expect(screen.getByText("桥面变形")).toBeInTheDocument();
    expect(screen.getByText("南京长江大桥")).toBeInTheDocument();
    expect(screen.getByText("杭州湾大桥")).toBeInTheDocument();
  });

  it("shows all columns for each event", () => {
    render(<EventTable events={mockEvents} selectedEventId="" onSelect={() => {}} onPlayback={() => {}} />);
    expect(screen.getByText("14:31:45")).toBeInTheDocument();
    expect(screen.getByText("14:30:22")).toBeInTheDocument();
    expect(screen.getByText("高风险")).toBeInTheDocument();
    expect(screen.getByText("中风险")).toBeInTheDocument();
    expect(screen.getByText("白天")).toBeInTheDocument();
  });

  it("highlights the selected row", () => {
    render(<EventTable events={mockEvents} selectedEventId="EV-001" onSelect={() => {}} onPlayback={() => {}} />);
    const rows = document.querySelectorAll("tbody tr");
    expect(rows[0].className).toContain("text-white");
  });

  it("calls onSelect when detail button clicked", async () => {
    const onSelect = vi.fn();
    const user = userEvent.setup();
    render(<EventTable events={mockEvents} selectedEventId="" onSelect={onSelect} onPlayback={() => {}} />);
    const buttons = screen.getAllByText("详情");
    await user.click(buttons[0]);
    expect(onSelect).toHaveBeenCalledWith("EV-001");
  });

  it("calls onPlayback when playback button clicked", async () => {
    const onPlayback = vi.fn();
    const user = userEvent.setup();
    render(<EventTable events={mockEvents} selectedEventId="" onSelect={() => {}} onPlayback={onPlayback} />);
    const buttons = screen.getAllByText("回放");
    await user.click(buttons[0]);
    expect(onPlayback).toHaveBeenCalledWith("EV-001");
  });
});
