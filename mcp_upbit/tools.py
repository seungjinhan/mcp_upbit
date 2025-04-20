from typing import List, Dict, Any

def get_available_tools() -> List[Dict[str, Any]]:
    """사용 가능한 도구 목록을 반환합니다."""
    return [
        {
            "name": "echo",
            "description": "Echoes back the input parameters",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    }
                }
            }
        },
        {
            "name": "calculator",
            "description": "Performs basic mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
        # 여기에 더 많은 도구를 추가할 수 있습니다
    ]