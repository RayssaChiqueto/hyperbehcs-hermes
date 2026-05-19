from __future__ import annotations

from dataclasses import dataclass

DESCRIPTOR_STATUS = {
    "AUTHORITY_DESCRIBED",
    "CHAIN_ROOT",
    "CHAIN_LINK",
    "PUBLIC_DESCRIPTOR",
}

PROMOTION_STATUS = {
    "PROMOTION_REQUESTED",
    "PROMOTION_APPROVED",
    "PROMOTION_DENIED",
    "PROMOTION_REVOKED",
    "PROMOTION_EXPIRED",
}

LEGACY_CLOSED_FIELDS = (
    "json",
    "runtime",
    "promote",
    "endpoint",
    "provider",
    "mcp",
    "usb_write",
    "device_write",
)

EXECUTION_FIELDS = (
    "dispatch",
    "route",
    "shell",
    "terminal",
    "file_write",
    "memory_write",
    "tool_execute",
    "skill_execute",
    "mcp_execute",
    "webmcp_execute",
    "provider_call",
    "endpoint_open",
    "browser_control",
    "keyboard_control",
    "screenshot_capture",
    "network_call",
    "webhook_open",
    "cron_create",
    "device_read",
    "device_write",
    "usb_read",
    "usb_write",
    "private_surface_export",
    "hidden_surface_export",
    "restricted_surface_export",
    "secret_surface_export",
    "repo_publish",
    "package_release",
)

AUTHORITY_FIELDS = tuple(dict.fromkeys((*LEGACY_CLOSED_FIELDS, *EXECUTION_FIELDS)))

DESCRIBE_ONLY_FIELDS = (
    "memory_read",
    "skill_read",
    "tool_describe",
    "mcp_describe",
    "webmcp_describe",
    "provider_describe",
    "browser_observe",
)


@dataclass(frozen=True)
class AuthorityDescriptor:
    name: str
    field: str
    category: str
    default: str = "0"
    description: str = ""


def describe_authority_surface() -> list[AuthorityDescriptor]:
    return [
        AuthorityDescriptor("memory_read", "memory_read", "memory", "1", "read already-public packet memory descriptors"),
        AuthorityDescriptor("memory_write", "memory_write", "memory", "0", "write or mutate memory/canon"),
        AuthorityDescriptor("skill_read", "skill_read", "skill", "1", "read public skill descriptor metadata"),
        AuthorityDescriptor("skill_execute", "skill_execute", "skill", "0", "execute a skill workflow"),
        AuthorityDescriptor("tool_describe", "tool_describe", "tool", "1", "describe a tool catalog entry"),
        AuthorityDescriptor("tool_execute", "tool_execute", "tool", "0", "execute a tool call"),
        AuthorityDescriptor("mcp_describe", "mcp_describe", "mcp", "1", "describe MCP server/tool metadata"),
        AuthorityDescriptor("mcp_execute", "mcp_execute", "mcp", "0", "call an MCP tool"),
        AuthorityDescriptor("webmcp_describe", "webmcp_describe", "webmcp", "1", "describe WebMCP bridge metadata"),
        AuthorityDescriptor("webmcp_execute", "webmcp_execute", "webmcp", "0", "open or call a WebMCP bridge"),
        AuthorityDescriptor("provider_describe", "provider_describe", "provider", "1", "describe provider/model metadata"),
        AuthorityDescriptor("provider_call", "provider_call", "provider", "0", "call a provider/model endpoint"),
        AuthorityDescriptor("endpoint_open", "endpoint_open", "network", "0", "publish/listen/open endpoint"),
        AuthorityDescriptor("browser_observe", "browser_observe", "browser", "1", "observe public browser surface"),
        AuthorityDescriptor("browser_control", "browser_control", "browser", "0", "control browser interactions"),
        AuthorityDescriptor("keyboard_control", "keyboard_control", "device", "0", "send keyboard input"),
        AuthorityDescriptor("screenshot_capture", "screenshot_capture", "device", "0", "capture screen contents"),
        AuthorityDescriptor("shell", "shell", "runtime", "0", "run shell command"),
        AuthorityDescriptor("terminal", "terminal", "runtime", "0", "open terminal execution"),
        AuthorityDescriptor("dispatch", "dispatch", "agent", "0", "dispatch agent work"),
        AuthorityDescriptor("route", "route", "agent", "0", "route capability/work to another surface"),
        AuthorityDescriptor("file_write", "file_write", "filesystem", "0", "write files"),
        AuthorityDescriptor("device_read", "device_read", "device", "0", "read device/USB surfaces"),
        AuthorityDescriptor("device_write", "device_write", "device", "0", "write device surfaces"),
        AuthorityDescriptor("usb_read", "usb_read", "device", "0", "read USB surfaces"),
        AuthorityDescriptor("usb_write", "usb_write", "device", "0", "write USB surfaces"),
        AuthorityDescriptor("private_surface_export", "private_surface_export", "boundary", "0", "export private surfaces"),
        AuthorityDescriptor("hidden_surface_export", "hidden_surface_export", "boundary", "0", "export hidden surfaces"),
        AuthorityDescriptor("restricted_surface_export", "restricted_surface_export", "boundary", "0", "export restricted surfaces"),
        AuthorityDescriptor("secret_surface_export", "secret_surface_export", "boundary", "0", "export secret surfaces"),
        AuthorityDescriptor("repo_publish", "repo_publish", "release", "0", "publish repository changes"),
        AuthorityDescriptor("package_release", "package_release", "release", "0", "publish package/release artifact"),
    ]
