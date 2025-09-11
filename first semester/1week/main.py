def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f'Error: {file_path} 파일을 찾을 수 없습니다.')
        return []
    except Exception as e:
        print(f'Error: 파일을 읽는 중 오류 발생 - {e}')
        return []


def parse_log(lines):
    return sorted(lines, reverse=True)


def extract_problematic_logs(lines):
    keywords = ['unstable', 'explosion', 'powered down']
    return [line for line in lines if any(keyword in line for keyword in keywords)]


def save_to_file(file_path, lines):
    try:
        with open(file_path, 'w') as file:
            file.writelines(lines)
    except Exception as e:
        print(f'Error: 파일 저장 중 오류 발생 - {e}')


def main():
    # print('Hello Mars')

    log_file = 'mission_computer_main.log'
    error_log_file = 'problem.log'

    # 1. 로그 파일 읽기
    logs = read_log_file(log_file)
    if not logs:
        return

    # 2. 로그 역순 정렬
    sorted_logs = parse_log(logs)

    # 3. 콘솔 출력
    for log in sorted_logs:
        print(log.strip())

    # 4. 문제 발생 로그 저장
    problematic_logs = extract_problematic_logs(sorted_logs)
    save_to_file(error_log_file, problematic_logs)


if __name__ == '__main__':
    main()
