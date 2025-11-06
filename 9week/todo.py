# 실행 방법 : python3 todo.py
# 테스트 명령어
#   - Todo 추가
#   curl -X POST http://localhost:8000/add_todo -H "Content-Type: application/json" -d '{"task": "과제하기", "description": "FastAPI 프로젝트"}'
#   - Todo 목록 조회
#   curl -X GET http://localhost:8000/retrieve_todo

from fastapi import FastAPI, APIRouter, HTTPException, Request
from typing import Dict, List, Any
import uvicorn
import json


todo_list: List[Dict] = []


router = APIRouter()


"""
todo_list에 새로운 항목을 추가합니다.

Args:
    request: HTTP 요청 객체
    
Returns:
    추가된 todo 항목과 성공 메시지를 포함한 Dict
"""


@router.post('/add_todo', response_model=Dict)
async def add_todo(request: Request) -> Dict:
    try:
        body = await request.json()
        todo_item = body if isinstance(body, dict) else {}
    except (json.JSONDecodeError, ValueError):
        # 입력이 올바르지 않으면 HTTP 400 오류 응답
        raise HTTPException(status_code=400, detail='입력이 올바르지 않습니다.')

    new_todo = dict(todo_item)
    todo_list.append(new_todo)

    return {
        'status': 'success',
        'message': 'Todo 항목이 성공적으로 추가되었습니다.',
        'todo': new_todo
    }


"""
todo_list를 가져옵니다.

Returns:
    todo_list를 포함한 Dict
"""


@router.get('/retrieve_todo', response_model=Dict)
def retrieve_todo() -> Dict:
    return {
        'todos': todo_list,
        'count': len(todo_list)
    }


app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
