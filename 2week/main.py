# python 기본 내장 모듈
import csv
import pickle


def read_csv_file(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f'Error: {file_path} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: 파일을 읽는 중 오류 발생 - {e}')
    return ''


def convert_to_list(file_path):
    inventory = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            lines = file.readlines()

        header = lines[0].strip().split(',')
        flammability_index = header.index('Flammability')

        for line in lines[1:]:
            row = line.strip().split(',')
            row[flammability_index] = float(row[flammability_index])

            inventory.append(row)

        return header, inventory
    except Exception as e:
        print(f'Error: CSV 변환 중 오류 발생 - {e}')
        return [], []


def sort_by_flammability(header, inventory):
    index = header.index('Flammability')
    # # 인화성 값을 float으로 변환해서 정렬
    # def get_flammability(row):
    #     try:
    #         return float(row[index])
    #     except ValueError:
    #         return -1  # 숫자로 변환 불가능한 값은 가장 낮게 취급

    return sorted(inventory, key=lambda x: x[index], reverse=True)


def save_as_binary(file_path, data):
    try:
        with open(file_path, mode='wb') as file:
            for row in data:
                # 리스트를 문자열로 바꾸고 줄바꿈 추가
                line = ','.join(map(str, row)) + '\n'
                # 문자열을 바이트로 인코딩해서 저장
                file.write(line.encode('utf-8'))
    except Exception as e:
        print(f'Error: 파일 저장 중 오류 발생 - {e}')


def read_binary_file(file_path):
    data = []
    try:
        with open(file_path, mode='rb') as file:
            for line in file:
                # 바이너리 → 문자열 디코딩
                decoded = line.decode('utf-8').strip()
                row = decoded.split(',')

                # 마지막 값이 숫자(Flammability)라고 가정하고 float으로 변환
                try:
                    row[-1] = float(row[-1])
                except ValueError:
                    row[-1] = -1.0  # 변환 실패 시 기본값
                data.append(row)

        return data
    except FileNotFoundError:
        print(f'Error: {file_path} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: 파일을 읽는 중 오류 발생 - {e}')
        return []


def filter_dangerous_items(header, inventory, threshold=0.7):
    index = header.index("Flammability")
    filtered = []

    for row in inventory:
        try:
            if row[index] >= threshold:
                filtered.append(row)
        except ValueError:
            continue  # 숫자로 변환 불가능한 값은 무시

    return filtered


def save_to_csv(file_path, header, items):
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # 컬럼명 포함
            for row in items:
                writer.writerow(row)
    except Exception as e:
        print(f'Error: 파일 저장 중 오류 발생 - {e}')


def print_inventory(title, inventory):
    print(title)
    for item in inventory:
        print(item)


def main():
    csv_path = 'data/Mars_Base_Inventory_List.csv'
    bin_path = 'data/Mars_Base_Inventory_List.bin'
    danger_csv_path = 'data/Mars_Base_Inventory_danger.csv'

    # CSV 파일 내용 출력
    print("CSV 파일 내용:")
    print(read_csv_file(csv_path))

    # 리스트로 변환
    header, inventory = convert_to_list(csv_path)

    # 인화성 내림차순 정렬
    sorted_inventory = sort_by_flammability(header, inventory)

    # 이진 파일로 저장
    save_as_binary(bin_path, sorted_inventory)

    # 이진 파일 출력
    binary_file = read_binary_file(bin_path)
    print_inventory("\n이진 파일에서 불러온 내용:", binary_file)

    # 인화성 ≥ 0.7 항목 필터링 및 출력
    danger_items = filter_dangerous_items(header, sorted_inventory)
    print_inventory("\n인화성 0.7 이상 위험 물품:", danger_items)

    # 위험 항목 CSV 저장
    save_to_csv(danger_csv_path, header, danger_items)


if __name__ == '__main__':
    main()
