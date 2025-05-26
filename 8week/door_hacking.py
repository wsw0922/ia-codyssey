import zipfile
import itertools
import string
import time

# ✅ mars 패턴 우선 탐색을 위한 함수
def generate_mars_passwords():
    chars = string.digits + string.ascii_lowercase
    results = set()

    # mars + 2자리
    for c1 in chars:
        for c2 in chars:
            results.add(f"mars{c1}{c2}")

    # 1자리 + mars + 1자리
    for c1 in chars:
        for c2 in chars:
            results.add(f"{c1}mars{c2}")

    # 2자리 + mars
    for c1 in chars:
        for c2 in chars:
            results.add(f"{c1}{c2}mars")

    return list(results)


def unlock_zip():
    zip_path = 'data/emergency_storage_key.zip'
    output_path = '8week/password.txt'
    total_attempts = 0
    found = False
    start_time = time.time()


    with zipfile.ZipFile(zip_path) as zf:
        # ✅ 1단계: mars 패턴 우선 시도
        print("[INFO] 'mars' 패턴 우선 탐색 시작...")
        for password in generate_mars_passwords():
            total_attempts += 1
            try:
                zf.extractall(pwd=password.encode())
                elapsed_time = time.time() - start_time
                print("[SUCCESS] 암호를 찾았습니다! (패턴 탐색)")
                print(f"비밀번호: {password}")
                print(f"총 시도 횟수: {total_attempts}")
                print(f"총 소요 시간: {elapsed_time:.2f}초")
                with open(output_path, 'w') as f:
                    f.write(f"비밀번호: {password}\n")
                    f.write(f"총 시도 횟수: {total_attempts}\n")
                    f.write(f"총 소요 시간: {elapsed_time:.2f}초\n")
                return
            except Exception:
                pass

        # ✅ 2단계: 일반 brute-force 탐색
        print("[INFO] 일반 brute-force 탐색 시작...")
        chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
        for pwd_tuple in itertools.product(chars, repeat=6):
            password = ''.join(pwd_tuple)
            total_attempts += 1

            if total_attempts % 100000 == 0:
                elapsed = time.time() - start_time
                print(f"[LOG] {total_attempts}회 시도 중... 경과 시간: {elapsed:.2f}초")
                print(f"현재까지 검증해본 암호 {password} 입니다.")

            try:
                zf.extractall(pwd=password.encode())
                elapsed_time = time.time() - start_time
                print("[SUCCESS] 암호를 찾았습니다!")
                print(f"비밀번호: {password}")
                print(f"총 시도 횟수: {total_attempts}")
                print(f"총 소요 시간: {elapsed_time:.2f}초")
                with open(output_path, 'w') as f:
                    f.write(f"비밀번호: {password}\n")
                    f.write(f"총 시도 횟수: {total_attempts}\n")
                    f.write(f"총 소요 시간: {elapsed_time:.2f}초\n")
                found = True
                break
            except Exception:
                pass

    if not found:
        print("[FAILED] 비밀번호를 찾지 못했습니다.")

if __name__ == '__main__':
    unlock_zip()
