# 실행 방법 : python3 todo.py
# 테스트 명령어
#   - Todo 추가
#   curl -X POST http://localhost:8000/add_todo \
#     -H 'Content-Type: application/json' \
#     -d '{"task": "과제하기", "description": "FastAPI 프로젝트"}'
#   - Todo 목록 조회
#   curl -X GET http://localhost:8000/retrieve_todo

from fastapi import FastAPI, APIRouter, HTTPException, Request
from typing import Dict, List
from model import TodoItem
import uvicorn
import csv
import os


CSV_FILE_PATH = 'todos.csv'
todo_list: List[Dict] = []
next_id: int = 1

router = APIRouter()


def load_todos_from_csv() -> None:
    """CSV 파일에서 todo 목록을 읽어 todo_list에 로드합니다."""
    global next_id

    if not os.path.exists(CSV_FILE_PATH):
        return

    with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        max_id = 0
        for row in reader:
            try:
                todo_id = int(row.get('id', '0'))
            except ValueError:
                continue

            task = row.get('task', '')
            description = row.get('description', '')

            todo = {
                'id': todo_id,
                'task': task,
                'description': description,
            }
            todo_list.append(todo)
            if todo_id > max_id:
                max_id = todo_id

        next_id = max_id + 1 if max_id > 0 else 1


def save_todos_to_csv() -> None:
    """todo_list 내용을 CSV 파일로 저장합니다."""
    fieldnames = ['id', 'task', 'description']

    with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for todo in todo_list:
            writer.writerow(todo)


def get_next_id() -> int:
    """새로운 todo 항목에 사용할 고유 id 값을 반환합니다."""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id


@router.post('/add_todo', response_model=Dict)
async def add_todo(request: Request) -> Dict:
    """
    todo_list에 새로운 항목을 추가합니다.

    Args:
        request: HTTP 요청 객체

    Returns:
        추가된 todo 항목과 성공 메시지를 포함한 Dict
    """
    try:
        body = await request.json()
        todo_item = body if isinstance(body, dict) else {}
    except ValueError:
        raise HTTPException(status_code=400, detail='입력이 올바르지 않습니다.')

    task = todo_item.get('task')
    description = todo_item.get('description')

    if not task or not isinstance(task, str):
        raise HTTPException(status_code=400, detail='task 필드는 필수 문자열입니다.')
    if description is None:
        description = ''

    new_todo = {
        'id': get_next_id(),
        'task': task,
        'description': description,
    }
    todo_list.append(new_todo)
    save_todos_to_csv()

    return {
        'status': 'success',
        'message': 'Todo 항목이 성공적으로 추가되었습니다.',
        'todo': new_todo,
    }


@router.get('/retrieve_todo', response_model=Dict)
def retrieve_todo() -> Dict:
    """
    todo_list 전체를 가져옵니다.

    Returns:
        todo_list와 개수를 포함한 Dict
    """
    return {
        'todos': todo_list,
        'count': len(todo_list),
    }


@router.get('/todo/{todo_id}', response_model=Dict)
def get_single_todo(todo_id: int) -> Dict:
    """
    단일 todo 항목을 id로 조회합니다.

    Args:
        todo_id: 조회할 todo의 id

    Returns:
        해당 id의 todo 항목을 포함한 Dict
    """
    for todo in todo_list:
        if todo.get('id') == todo_id:
            return {'todo': todo}

    raise HTTPException(status_code=404, detail='해당 id의 Todo 항목을 찾을 수 없습니다.')


@router.put('/todo/{todo_id}', response_model=Dict)
async def update_todo(todo_id: int, item: TodoItem) -> Dict:
    """
    단일 todo 항목을 id로 수정합니다.

    Args:
        todo_id: 수정할 todo의 id
        item: 수정할 내용을 담은 TodoItem 모델

    Returns:
        수정된 todo 항목과 메시지를 포함한 Dict
    """
    for index, todo in enumerate(todo_list):
        if todo.get('id') == todo_id:
            updated_todo = {
                'id': todo_id,
                'task': item.task,
                'description': item.description,
            }
            todo_list[index] = updated_todo
            save_todos_to_csv()
            return {
                'status': 'success',
                'message': 'Todo 항목이 성공적으로 수정되었습니다.',
                'todo': updated_todo,
            }

    raise HTTPException(status_code=404, detail='해당 id의 Todo 항목을 찾을 수 없습니다.')


@router.delete('/todo/{todo_id}', response_model=Dict)
def delete_single_todo(todo_id: int) -> Dict:
    """
    단일 todo 항목을 id로 삭제합니다.

    Args:
        todo_id: 삭제할 todo의 id

    Returns:
        삭제된 todo 항목과 메시지를 포함한 Dict
    """
    for index, todo in enumerate(todo_list):
        if todo.get('id') == todo_id:
            deleted_todo = todo_list.pop(index)
            save_todos_to_csv()
            return {
                'status': 'success',
                'message': 'Todo 항목이 성공적으로 삭제되었습니다.',
                'todo': deleted_todo,
            }

    raise HTTPException(status_code=404, detail='해당 id의 Todo 항목을 찾을 수 없습니다.')


app = FastAPI()
app.include_router(router)

# 서버 시작 전에 CSV에서 기존 데이터 로드
load_todos_from_csv()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)