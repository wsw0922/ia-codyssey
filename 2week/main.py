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
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # 헤더 저장
        for row in reader:
            if len(row) != len(header):
                continue  # 컬럼 수 안 맞으면 건너뜀
            inventory.append(row)
    return header, inventory


def sort_by_flammability(header, inventory):
    try:
        index = header.index('Flammability')
    except ValueError:
        print("Error: 'Flammability' 컬럼을 찾을 수 없습니다.")
        return inventory

    # 인화성 값을 float으로 변환해서 정렬
    def get_flammability(row):
        try:
            return float(row[index])
        except ValueError:
            return -1  # 숫자로 변환 불가능한 값은 가장 낮게 취급

    return sorted(inventory, key=get_flammability, reverse=True)


def save_as_binary(file_path, data):
    try:
        with open(file_path, mode='wb') as file:
            pickle.dump(data, file)
    except Exception as e:
        print(f'Error: 파일 저장 중 오류 발생 - {e}')


def read_binary_file(file_path):
    try:
        with open(file_path, mode='rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f'Error: {file_path} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: 파일을 읽는 중 오류 발생 - {e}')


def filter_dangerous_items(header, inventory, threshold=0.7):
    try:
        index = header.index("Flammability")
    except ValueError:
        print("Error: 'Flammability' 컬럼을 찾을 수 없습니다.")
        return []

    filtered = []
    for row in inventory:
        try:
            if float(row[index]) >= threshold:
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
