from string import ascii_lowercase as ALPHABET

def casesar_cipher_decode(target_text):
    
    print("[INFO] 시저 암호 복호화 결과 (0~25): \n")
    
    for shift in range(26):
        decoded = ''
        for char in target_text:
            if char.islower():
                idx = (ALPHABET.index(char) - shift) % 26
                decoded += ALPHABET[idx]
            elif char.isupper():
                idx = (ord(char) - ord('A') - shift) % 26
                decoded += chr(idx + ord('A'))
            else:
                decoded += char
        print(f"{shift:2} {decoded}")
    
def read_password_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()


def save_result(result_text, output_path):
    with open(output_path, 'w') as f:
        f.write(result_text)


def main():
    input_path = "data/password.txt"
    output_path = "result.txt"

    try:
        text = read_password_file(input_path)
    except Exception as e:
        print("[ERROR] 파일을 읽을 수 없습니다. :{e}")
        return

    print(f"[INFO] password.txt 파일 내용:")
    print(text)
    print("\n")

    casesar_cipher_decode(text)

    shift = input("\n[*] 복호화된 문장이 맞다고 생각되는 시프트 값을 입력하세요 (0~25): ")
    try:
        shift = int(shift)
        from string import ascii_lowercase as ALPHABET
        decoded = ''
        for char in text:
            if char.islower():
                idx = (ALPHABET.index(char) - shift) % 26
                decoded += ALPHABET[idx]
            elif char.isupper():
                idx = (ord(char) - ord('A') - shift) % 26
                decoded += chr(idx + ord('A'))
            else:
                decoded += char

        save_result(decoded, output_path)
        print(f"[INFO] 복호화 결과가 {output_path}에 저장되었습니다.")
    except:
        print("[ERROR] 유효한 숫자를 입력하세요 (0~25)")

if __name__ == '__main__':
    main()