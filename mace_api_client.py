"""Mace Accounts API client and shared server-address loader.

Edit the first non-empty line of mace_server.txt to change the API endpoint.
Accepted examples:
  127.0.0.1:8000
  203.0.113.10:8000
  https://accounts.example.com
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional

DEFAULT_SERVER = "http://127.0.0.1:8000"
CONFIG_NAME = "mace_server.txt"


def app_directory() -> Path:
    """Use the EXE folder for frozen builds and source folder for development."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def normalize_server_address(value: str) -> str:
    value = str(value or "").strip().strip('"').strip("'")
    if not value or value.startswith("#"):
        return DEFAULT_SERVER
    value = value.rstrip("/")
    if value.startswith("//"):
        value = "http:" + value
    elif "://" not in value:
        # An unqualified IPv4/domain/host:port means HTTP API. Port 8000 is
        # the local default; an explicitly entered port is respected.
        if value.count(":") == 0:
            value = f"{value}:8000"
        value = "http://" + value
    from urllib.parse import urlsplit, urlunsplit
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        return DEFAULT_SERVER
    # Do not let typo-prone entries silently send requests to an arbitrary scheme.
    if any(ch.isspace() for ch in parsed.netloc):
        return DEFAULT_SERVER
    return urlunsplit((parsed.scheme.lower(), parsed.netloc, parsed.path.rstrip("/"), "", ""))


def server_config_path() -> Path:
    return app_directory() / CONFIG_NAME


def read_server_url(config_path: Optional[os.PathLike | str] = None) -> str:
    """Read the server URL fresh on every call so editing the TXT takes effect."""
    path = Path(config_path) if config_path else server_config_path()
    try:
        if not path.exists():
            path.write_text(DEFAULT_SERVER + "\n", encoding="utf-8")
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return normalize_server_address(line)
    except OSError:
        pass
    return DEFAULT_SERVER


class MaceAPIError(RuntimeError):
    def __init__(self, message: str, status_code: int = 0, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class MaceAPIClient:
    """Small standard-library-only client for MaceHost.py."""
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    @property
    def base_url(self) -> str:
        return read_server_url()

    def request(self, method: str, endpoint: str, payload: Optional[dict] = None,
                token: Optional[str] = None) -> dict:
        base_url = self.base_url
        url = base_url + "/" + endpoint.lstrip("/")
        headers = {"Accept": "application/json", "User-Agent": "MaceLauncher/Accounts"}
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if token:
            headers["Authorization"] = "Bearer " + token
        request = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8", errors="replace")
                result = json.loads(raw) if raw else {}
                return result if isinstance(result, dict) else {"data": result}
        except urllib.error.HTTPError as exc:
            try:
                raw = exc.read().decode("utf-8", errors="replace")
                result = json.loads(raw) if raw else {}
            except Exception:
                result = {}
            detail = result.get("detail") or result.get("message") or f"HTTP {exc.code}"
            raise MaceAPIError(str(detail), exc.code, result) from exc
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise MaceAPIError(
                f"Не удалось подключиться к серверу Mace: {base_url}. Проверьте mace_server.txt и доступность сервера.",
                0,
            ) from exc

    def health(self) -> dict:
        return self.request("GET", "/health")

    def register(self, username: str, email: str, password: str) -> dict:
        return self.request("POST", "/register", {"username": username, "email": email, "password": password})

    def login(self, username: str, password: str) -> dict:
        return self.request("POST", "/login", {"username": username, "password": password})

    def me(self, token: str) -> dict:
        return self.request("GET", "/me", token=token)

    def logout(self, token: str) -> dict:
        return self.request("POST", "/logout", token=token)

    def search_users(self, token: str, query: str) -> dict:
        return self.request("GET", "/users/search?q=" + urllib.parse.quote(query), token=token)

    def friends(self, token: str) -> dict:
        return self.request("GET", "/friends", token=token)

    def send_friend_request(self, token: str, mace_id: str) -> dict:
        return self.request("POST", "/friends/request", {"mace_id": mace_id}, token=token)

    def respond_friend_request(self, token: str, request_id: int, accept: bool) -> dict:
        action = "accept" if accept else "reject"
        return self.request("POST", f"/friends/requests/{int(request_id)}/{action}", {}, token=token)

    def remove_friend(self, token: str, mace_id: str) -> dict:
        return self.request("DELETE", "/friends/" + urllib.parse.quote(mace_id, safe=""), token=token)

    def block_user(self, token: str, mace_id: str) -> dict:
        return self.request("POST", "/users/block", {"mace_id": mace_id}, token=token)

    def unblock_user(self, token: str, mace_id: str) -> dict:
        return self.request("DELETE", "/users/block/" + urllib.parse.quote(mace_id, safe=""), token=token)
