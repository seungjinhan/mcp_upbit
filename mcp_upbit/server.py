import json
import sys
import traceback
from typing import Dict, Any, List

# stderr로 디버깅 메시지 출력
sys.stderr.write("서버 시작 중...\n")
sys.stderr.flush()

# tools.py에서 함수 가져오기
from .tools import get_available_tools

class MCPServer:
    def __init__(self):
        sys.stderr.write("MCPServer 초기화 중...\n")
        sys.stderr.flush()
        self.tools = get_available_tools()
        self.initialized = False
    
    def _read_message(self) -> Dict[str, Any]:
        """메시지를 읽고 파싱합니다."""
        sys.stderr.write("입력 대기 중...\n")
        sys.stderr.flush()
        try:
            line = sys.stdin.readline()
            if not line:
                sys.stderr.write("빈 입력 수신, 종료합니다.\n")
                sys.stderr.flush()
                sys.exit(0)
            sys.stderr.write(f"수신된 입력: {line.strip()}\n")
            sys.stderr.flush()
            return json.loads(line)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"JSON 파싱 오류: {e}\n")
            sys.stderr.flush()
            return {"type": "error", "error": "Invalid JSON"}

    def _write_message(self, message: Dict[str, Any]) -> None:
        """메시지를 JSON 형식으로 작성합니다."""
        # 요청에 jsonrpc 필드가 있었다면 응답에도 추가
        if "id" in message and "jsonrpc" not in message:
            message["jsonrpc"] = "2.0"
        
        sys.stderr.write(f"응답 전송: {message}\n")
        sys.stderr.flush()
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()

    def _handle_initialize(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """초기화 요청을 처리합니다."""
        sys.stderr.write("Initialize 요청 처리 중...\n")
        sys.stderr.flush()
        
        # 요청 ID 추출
        req_id = message.get("id")
        
        # 요청 파라미터 출력 (디버깅용)
        params = message.get("params", {})
        sys.stderr.write(f"Initialize 파라미터: {params}\n")
        sys.stderr.flush()
        
        self.initialized = True
        response = {
            "type": "initialize_response",
            "server_info": {
                "name": "Simple Python MCP Server",
                "version": "1.0.0",
                "description": "A simple MCP server implemented in Python"
            }
        }
        
        # ID가 있으면 응답에 포함
        if req_id is not None:
            response["id"] = req_id
        
        return response

    def _handle_tools_list(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """도구 목록 요청을 처리합니다."""
        sys.stderr.write("Tools List 요청 처리 중...\n")
        sys.stderr.flush()
        
        # 요청 ID 추출
        req_id = message.get("id")
        
        response = {
            "type": "tools_list_response",
            "tools": self.tools
        }
        
        # ID가 있으면 응답에 포함
        if req_id is not None:
            response["id"] = req_id
        
        return response

    def _handle_tool_call(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """도구 호출 요청을 처리합니다."""
        call_id = message.get("call_id", "")
        tool_name = message.get("tool_name", "")
        parameters = message.get("parameters", {})
        
        # 요청 ID 추출
        req_id = message.get("id")
        
        # 메서드 형식일 경우 파라미터 추출
        if "params" in message and (not tool_name or not parameters):
            params = message.get("params", {})
            if not tool_name and "name" in params:
                tool_name = params.get("name", "")
            if not parameters and "parameters" in params:
                parameters = params.get("parameters", {})
            if not call_id and "call_id" in params:
                call_id = params["call_id"]
        
        sys.stderr.write(f"Tool Call 요청 처리 중: {tool_name}, 파라미터: {parameters}\n")
        sys.stderr.flush()
        
        try:
            # 도구 이름이 유효한지 확인
            tool_exists = any(tool["name"] == tool_name for tool in self.tools)
            if not tool_exists:
                sys.stderr.write(f"도구를 찾을 수 없음: {tool_name}\n")
                sys.stderr.flush()
                result = {
                    "type": "tool_call_response",
                    "call_id": call_id,
                    "status": "error",
                    "error": {
                        "type": "not_found",
                        "message": f"Tool '{tool_name}' not found"
                    }
                }
                if req_id is not None:
                    result["id"] = req_id
                return result
                
            # echo 도구 처리
            if tool_name == "echo":
                sys.stderr.write("Echo 도구 실행 중...\n")
                sys.stderr.flush()
                result = {
                    "type": "tool_call_response",
                    "call_id": call_id,
                    "status": "success",
                    "result": parameters
                }
                if req_id is not None:
                    result["id"] = req_id
                return result
                
            # 계산기 도구 처리
            if tool_name == "calculator":
                expression = parameters.get("expression", "")
                sys.stderr.write(f"Calculator 도구 실행 중: {expression}\n")
                sys.stderr.flush()
                try:
                    # 안전하게 계산하기 (eval 사용 주의)
                    # 실제 서비스에서는 더 안전한 방법을 사용해야 합니다
                    result = eval(expression, {"__builtins__": {}}, {})
                    response = {
                        "type": "tool_call_response",
                        "call_id": call_id,
                        "status": "success",
                        "result": {
                            "result": result
                        }
                    }
                    if req_id is not None:
                        response["id"] = req_id
                    return response
                except Exception as e:
                    sys.stderr.write(f"계산 오류: {str(e)}\n")
                    sys.stderr.flush()
                    result = {
                        "type": "tool_call_response",
                        "call_id": call_id,
                        "status": "error",
                        "error": {
                            "type": "calculation_error",
                            "message": f"Error calculating: {str(e)}"
                        }
                    }
                    if req_id is not None:
                        result["id"] = req_id
                    return result
            
            # 기본 응답
            sys.stderr.write(f"구현되지 않은 도구: {tool_name}\n")
            sys.stderr.flush()
            result = {
                "type": "tool_call_response",
                "call_id": call_id,
                "status": "error",
                "error": {
                    "type": "not_implemented",
                    "message": f"Tool '{tool_name}' is not implemented yet"
                }
            }
            if req_id is not None:
                result["id"] = req_id
            return result
            
        except Exception as e:
            sys.stderr.write(f"Tool Call 처리 중 오류: {str(e)}\n")
            sys.stderr.write(traceback.format_exc() + "\n")
            sys.stderr.flush()
            result = {
                "type": "tool_call_response",
                "call_id": call_id,
                "status": "error",
                "error": {
                    "type": "internal_error",
                    "message": str(e),
                    "traceback": traceback.format_exc()
                }
            }
            if req_id is not None:
                result["id"] = req_id
            return result

    def run(self) -> None:
        """서버 메인 루프."""
        sys.stderr.write("서버 메인 루프 시작...\n")
        sys.stderr.flush()
        while True:
            message = self._read_message()
            
            if not message:
                sys.stderr.write("빈 메시지 수신, 건너뜁니다.\n")
                sys.stderr.flush()
                continue
                
            # 메시지 형식 확인 - method와 params 형식 지원
            message_type = message.get("type", "")
            message_method = message.get("method", "")
            
            # JSONRPC 스타일 (method/params) 요청을 MCP 스타일 (type)으로 변환
            if message_method == "initialize" and not message_type:
                message_type = "initialize"
                sys.stderr.write(f"initialize 메서드 감지, type으로 변환합니다.\n")
            elif message_method == "tools.list" and not message_type:  # tools.list 형식도 처리
                message_type = "tools/list"
                sys.stderr.write(f"tools.list 메서드 감지, type으로 변환합니다.\n")
            elif message_method == "tools/list" and not message_type:
                message_type = "tools/list"
                sys.stderr.write(f"tools/list 메서드 감지, type으로 변환합니다.\n") 
            elif message_method == "tool.call" and not message_type:  # tool.call 형식도 처리
                message_type = "tool/call"
                sys.stderr.write(f"tool.call 메서드 감지, type으로 변환합니다.\n")
            elif message_method == "tool/call" and not message_type:
                message_type = "tool/call"
                sys.stderr.write(f"tool/call 메서드 감지, type으로 변환합니다.\n")
            
            sys.stderr.write(f"메시지 유형 수신: {message_type}\n")
            sys.stderr.flush()
            
            # initialize와 tools/list는 초기화 없이도 접근 가능
            if not self.initialized and message_type != "initialize" and message_type != "tools/list":
                sys.stderr.write("서버가 초기화되지 않았습니다.\n")
                sys.stderr.flush()
                response = {
                    "type": "error",
                    "error": "Server not initialized"
                }
                if "id" in message:
                    response["id"] = message["id"]
                    response["jsonrpc"] = "2.0"
                self._write_message(response)
                continue
            
            response = None
            
            if message_type == "initialize":
                response = self._handle_initialize(message)
            elif message_type == "tools/list":
                response = self._handle_tools_list(message)
            elif message_type == "tool/call":
                response = self._handle_tool_call(message)
            else:
                sys.stderr.write(f"알 수 없는 메시지 유형: {message_type}\n")
                sys.stderr.flush()
                response = {
                    "type": "error",
                    "error": f"Unknown message type: {message_type}"
                }
                if "id" in message:
                    response["id"] = message["id"]
                    response["jsonrpc"] = "2.0"
            
            if response:
                self._write_message(response)

def main():
    """메인 함수."""
    sys.stderr.write("main() 함수 실행 시작\n")
    sys.stderr.flush()
    server = MCPServer()
    server.run()

if __name__ == "__main__":
    sys.stderr.write("__main__ 블록 실행\n")
    sys.stderr.flush()
    main()