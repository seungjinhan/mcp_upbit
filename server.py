#!/usr/bin/env python3
# Hello World MCP Server in Python

import json
import sys
import traceback
from typing import Dict, Any, Optional


class MCPServer:
    def __init__(self):
        self.handlers = {}
    
    def register(self, method_name, handler):
        """등록된 메서드 핸들러를 저장합니다."""
        self.handlers[method_name] = handler
    
    def handle_request(self, request):
        """들어오는 MCP 요청을 처리합니다."""
        method = request.get("method")
        params = request.get("params", {})
        req_id = request.get("id")
        
        if method in self.handlers:
            try:
                result = self.handlers[method](params)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            except Exception as e:
                # 에러 처리
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32000,
                        "message": f"Internal error: {str(e)}",
                        "data": traceback.format_exc()
                    }
                }
        else:
            # 메서드를 찾을 수 없음
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    def start(self):
        """서버를 시작하고 stdin에서 요청을 받아 stdout으로 응답합니다."""
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError:
                sys.stderr.write(f"Invalid JSON received: {line}\n")
                sys.stderr.flush()
            except Exception as e:
                sys.stderr.write(f"Error processing request: {str(e)}\n")
                sys.stderr.flush()


# MCP 서버 인스턴스 생성
server = MCPServer()

# 서버 초기화 메서드 등록 (필수)
def initialize(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    print("Server initialized", file=sys.stderr)
    return {
        "name": "hello-world-mcp-python",
        "version": "1.0.0",
        "description": "A simple Hello World MCP server in Python"
    }

server.register("initialize", initialize)

# /tools/list 엔드포인트 구현 (필수)
def tools_list(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "hello_world",
                "description": "Returns a Hello World message",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Your name (optional)"
                        }
                    }
                }
            }
        ]
    }

server.register("/tools/list", tools_list)

# Hello World 도구 구현
def hello_world(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    name = params.get("name", "World") if params else "World"
    return {
        "message": f"Hello, {name}!"
    }

server.register("hello_world", hello_world)

# 메인 실행 부분
if __name__ == "__main__":
    print("Hello World MCP server is running...", file=sys.stderr)
    server.start()