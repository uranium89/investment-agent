import asyncio
import json
import logging
from pathlib import Path
from typing import Any
from pipeline.config import settings

logger = logging.getLogger(__name__)


class DNSEError(Exception):
    pass


class DNSEClient:
    def __init__(self, mcp_dir: str | None = None):
        self.mcp_dir = Path(mcp_dir or settings.dnse_mcp_dir).resolve()
        self.process: asyncio.subprocess.Process | None = None
        self._request_id = 0
        self._pending: dict[int, asyncio.Future] = {}
        self._reader_task: asyncio.Task | None = None

    async def __aenter__(self):
        await self._start()
        return self

    async def __aexit__(self, *args):
        await self._stop()

    async def _start(self):
        entry = self.mcp_dir / "build" / "index.js"
        if not entry.exists():
            raise FileNotFoundError(f"DNSE MCP server not found at {entry}")

        self.process = await asyncio.create_subprocess_exec(
            "node", str(entry),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.mcp_dir),
        )

        self._reader_task = asyncio.create_task(self._read_stdout())

        resp = await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "vn30-pipeline", "version": "0.1.0"},
        })

        if resp.get("error"):
            raise DNSEError(f"Initialize failed: {resp['error']}")

        await self._send_notification("notifications/initialized")
        logger.info("DNSE MCP client initialized")

    async def _stop(self):
        if self._reader_task:
            self._reader_task.cancel()
            self._reader_task = None
        if self.process and self.process.returncode is None:
            self.process.kill()
            await self.process.wait()
        for fut in self._pending.values():
            if not fut.done():
                fut.cancel()
        self._pending.clear()

    async def _read_stdout(self):
        try:
            while self.process and self.process.stdout:
                line = await self.process.stdout.readline()
                if not line:
                    break
                line = line.decode(errors="replace").strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg_id = msg.get("id")
                if msg_id is not None and msg_id in self._pending:
                    self._pending[msg_id].set_result(msg)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("DNSE MCP reader error: %s", e)

    async def _send_request(self, method: str, params: dict | None = None) -> dict:
        self._request_id += 1
        req_id = self._request_id
        req = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}}
        future = asyncio.get_event_loop().create_future()
        self._pending[req_id] = future
        try:
            await self._write_json(req)
            return await asyncio.wait_for(future, timeout=60)
        finally:
            self._pending.pop(req_id, None)

    async def _send_notification(self, method: str, params: dict | None = None):
        await self._write_json({"jsonrpc": "2.0", "method": method, "params": params or {}})

    async def _write_json(self, msg: dict):
        if not self.process or not self.process.stdin:
            raise DNSEError("DNSE MCP process not running")
        line = json.dumps(msg, ensure_ascii=False) + "\n"
        self.process.stdin.write(line.encode())
        await self.process.stdin.drain()

    def _parse_result(self, resp: dict) -> Any:
        if resp.get("error"):
            raise DNSEError(f"DNSE error: {resp['error']}")
        result = resp.get("result", {})
        content = result.get("content", [])
        if content and isinstance(content, list):
            text_parts = []
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    text_parts.append(c.get("text", ""))
            if text_parts:
                raw = "".join(text_parts)
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return {"raw": raw}
        return result

    async def call_tool(self, tool_name: str, arguments: dict | None = None) -> Any:
        resp = await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments or {},
        })
        return self._parse_result(resp)

    # ── Read-only market data wrappers ────────────────────────────────

    async def security_definition(self, symbol: str) -> dict:
        return await self.call_tool("dnse_security_definition", {"symbol": symbol})

    async def ohlc(self, symbol: str, resolution: str = "1D",
                   from_ts: int | None = None, to_ts: int | None = None) -> dict:
        params = {"symbol": symbol, "resolution": resolution}
        if from_ts:
            params["from"] = from_ts
        if to_ts:
            params["to"] = to_ts
        return await self.call_tool("dnse_ohlc", params)

    async def latest_trade(self, symbol: str) -> dict:
        return await self.call_tool("dnse_latest_trade", {"symbol": symbol})

    async def close_price(self, symbol: str) -> dict:
        return await self.call_tool("dnse_close_price", {"symbol": symbol})

    async def instruments(self, **kwargs) -> list[dict]:
        result = await self.call_tool("dnse_instruments", kwargs or {})
        if isinstance(result, dict):
            return result.get("data", [])
        return result if isinstance(result, list) else []

    async def working_dates(self) -> list[str]:
        result = await self.call_tool("dnse_working_dates", {})
        if isinstance(result, dict):
            return result.get("data", [])
        return result if isinstance(result, list) else []
