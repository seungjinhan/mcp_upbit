import json
import sys
from typing import Dict, Any

def read_json_rpc_message() -> Dict[str, Any]:
    """JSON-RPC 형식의 메시지를 표준 입력에서 읽습니다."""
    line = sys.stdin.readline()
    if not line:
        return {}
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return {}

def write_json_rpc_response(response: Dict[str, Any]) -> None:
    """JSON-RPC 형식의 응답을 표준 출력으로 전송합니다."""
    print(json.dumps(response), flush=True)

def handle_initialize(params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
    """초기화 요청을 처리합니다."""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "python-mcp-example",
                "version": "1.0.0"
            },
            "capabilities": {
                "defaultPrimitives": [
                    {
                        "name": "example_tool",
                        "description": "예시 도구입니다.",
                        "type": "function",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "검색 쿼리"
                                }
                            },
                            "required": ["query"]
                        },
                        "returns": {
                            "type": "string",
                            "description": "검색 결과"
                        }
                    }
                ]
            }
        }
    }

def handle_tools_list(params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
    """사용 가능한 도구 목록을 반환합니다."""
    # MCP 프로토콜에 맞는 정확한 응답 형식
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": [  # 직접 배열 반환
            {
                "name": "example_tool",
                "description": "예시 도구입니다.",
                "type": "function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "검색 쿼리"
                        }
                    },
                    "required": ["query"]
                },
                "returns": {
                    "type": "string",
                    "description": "검색 결과"
                }
            }
        ]
    }

def handle_example_tool(params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
    """예시 도구 기능을 구현합니다."""
    query = params.get("query", "")
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": f"쿼리 \"{query}\"에 대한 결과입니다."
    }

def main():
    """메인 서버 루프"""
    print("MCP 서버 시작...", file=sys.stderr)
    
    while True:
        try:
            # JSON-RPC 메시지 읽기
            line = sys.stdin.readline()
            if not line:
                continue
                
            print(f"원시 입력: {line.strip()}", file=sys.stderr)
            
            try:
                message = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 오류: {e}", file=sys.stderr)
                continue
            
            print(f"받은 메시지: {message}", file=sys.stderr)
                
            # 메시지 구성요소 추출
            message_id = message.get("id")
            method = message.get("method")
            params = message.get("params", {})
            
            # 알림 메시지인 경우 응답하지 않음 (id가 없는 경우)
            if message_id is None:
                print(f"알림 메시지 수신: {method}", file=sys.stderr)
                continue
            
            # 요청 유형에 따라 처리
            if method == "initialize":
                response = handle_initialize(params, message_id)
                print(f"초기화 응답: {response}", file=sys.stderr)
                write_json_rpc_response(response)
                
                # 초기화 응답에 기본 도구 목록을 포함시킴
                print("초기화 완료 (기본 도구 목록 포함)", file=sys.stderr)
                
            elif method == "tools/list":
                print("tools/list 메서드 처리 중...", file=sys.stderr)
                response = handle_tools_list(params, message_id)
                print(f"tools/list 응답: {response}", file=sys.stderr)
                write_json_rpc_response(response)
                
            elif method == "example_tool":
                response = handle_example_tool(params, message_id)
                print(f"example_tool 응답: {response}", file=sys.stderr)
                write_json_rpc_response(response)
                
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                print(f"알 수 없는 메서드 응답: {response}", file=sys.stderr)
                write_json_rpc_response(response)
            
        except Exception as e:
            # 오류 처리
            print(f"오류 발생: {str(e)}", file=sys.stderr)
            if 'message' in locals() and 'message_id' in locals() and message_id is not None:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                write_json_rpc_response(error_response)

if __name__ == "__main__":
    main()