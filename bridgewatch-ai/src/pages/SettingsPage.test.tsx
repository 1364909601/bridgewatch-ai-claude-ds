import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi } from "vitest";
import { SettingsPage } from "./SettingsPage";

vi.mock("../hooks/use-users", () => ({
  useUserList: () => ({
    data: {
      list: [
        { user_id: "u1", username: "admin", display_name: "系统管理员", role: "admin", is_active: true },
        { user_id: "u2", username: "operator", display_name: "值班操作员", role: "operator", is_active: true },
        { user_id: "u3", username: "viewer", display_name: "观察员", role: "viewer", is_active: false },
      ],
    },
    isLoading: false,
  }),
  useCreateUser: () => ({ mutate: vi.fn(), isPending: false }),
  useUpdateUser: () => ({ mutate: vi.fn(), isPending: false }),
  useDeleteUser: () => ({ mutate: vi.fn(), isPending: false }),
}));

function renderWithQuery(ui: React.ReactElement) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={qc}>{ui}</QueryClientProvider>);
}

describe("SettingsPage", () => {
  it("renders user management title", () => {
    renderWithQuery(<SettingsPage />);
    expect(screen.getByText("用户管理")).toBeInTheDocument();
  });

  it("shows user count", () => {
    renderWithQuery(<SettingsPage />);
    expect(screen.getByText("共 3 个用户")).toBeInTheDocument();
  });

  it("renders all users from mock", () => {
    renderWithQuery(<SettingsPage />);
    expect(screen.getByText("系统管理员")).toBeInTheDocument();
    expect(screen.getByText("值班操作员")).toBeInTheDocument();
    expect(screen.getByText("观察员")).toBeInTheDocument();
  });

  it("has add user button", () => {
    renderWithQuery(<SettingsPage />);
    expect(screen.getByText("添加用户")).toBeInTheDocument();
  });

  it("shows create form when add user clicked", async () => {
    const user = userEvent.setup();
    renderWithQuery(<SettingsPage />);
    await user.click(screen.getByText("添加用户"));
    expect(screen.getByPlaceholderText("用户名")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("密码")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("显示名称")).toBeInTheDocument();
  });

  it("renders alert config section", () => {
    renderWithQuery(<SettingsPage />);
    expect(screen.getByText("告警配置")).toBeInTheDocument();
    expect(screen.getByText("系统信息")).toBeInTheDocument();
  });
});
