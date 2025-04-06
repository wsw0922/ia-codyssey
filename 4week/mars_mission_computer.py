import random
import time


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        # 문제에서 제시된 항목으로 env_values 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        # 5분(60회) 동안의 기록 저장용
        self.records = []

    def get_sensor_data(self, sensor):
        count = 0

        while True:
            # 특정 키(S/s 등) 입력 시 종료
            user_input = input("Press 's' to stop or just press Enter to continue: ")
            if user_input.lower() == 's':
                print('System stoped....')
                break

            # 1. 센서값 갱신 후 가져오기
            sensor.set_env()
            self.env_values = sensor.get_env()

            # 2. 화면에 JSON 형태로 출력
            # (Python json 라이브러리 없이 직접 포매팅)
            json_str = (
                '{'
                f"\"mars_base_internal_temperature\": {self.env_values['mars_base_internal_temperature']}, "
                f"\"mars_base_external_temperature\": {self.env_values['mars_base_external_temperature']}, "
                f"\"mars_base_internal_humidity\": {self.env_values['mars_base_internal_humidity']}, "
                f"\"mars_base_external_illuminance\": {self.env_values['mars_base_external_illuminance']}, "
                f"\"mars_base_internal_co2\": {self.env_values['mars_base_internal_co2']}, "
                f"\"mars_base_internal_oxygen\": {self.env_values['mars_base_internal_oxygen']}"
                '}'
            )
            print(json_str)

            # 5분 평균 계산을 위해 기록 축적
            self.records.append(self.env_values.copy())
            count += 1

            # 3. 5분마다 평균값 별도 출력
            if count % 60 == 0:  # 5초 * 60 = 300초(5분)
                avg_values = {
                    'mars_base_internal_temperature': 0.0,
                    'mars_base_external_temperature': 0.0,
                    'mars_base_internal_humidity': 0.0,
                    'mars_base_external_illuminance': 0.0,
                    'mars_base_internal_co2': 0.0,
                    'mars_base_internal_oxygen': 0.0
                }

                # 누적된 60번(5분) 데이터를 합산
                for record in self.records:
                    avg_values['mars_base_internal_temperature'] += record['mars_base_internal_temperature']
                    avg_values['mars_base_external_temperature'] += record['mars_base_external_temperature']
                    avg_values['mars_base_internal_humidity'] += record['mars_base_internal_humidity']
                    avg_values['mars_base_external_illuminance'] += record['mars_base_external_illuminance']
                    avg_values['mars_base_internal_co2'] += record['mars_base_internal_co2']
                    avg_values['mars_base_internal_oxygen'] += record['mars_base_internal_oxygen']

                # 평균 계산
                size = len(self.records)
                for key in avg_values:
                    avg_values[key] /= size

                # 평균값 JSON 형태로 출력
                avg_json_str = (
                    '{'
                    f"\"mars_base_internal_temperature\": {avg_values['mars_base_internal_temperature']}, "
                    f"\"mars_base_external_temperature\": {avg_values['mars_base_external_temperature']}, "
                    f"\"mars_base_internal_humidity\": {avg_values['mars_base_internal_humidity']}, "
                    f"\"mars_base_external_illuminance\": {avg_values['mars_base_external_illuminance']}, "
                    f"\"mars_base_internal_co2\": {avg_values['mars_base_internal_co2']}, "
                    f"\"mars_base_internal_oxygen\": {avg_values['mars_base_internal_oxygen']}"
                    '}'
                )
                print('[5분 평균]', avg_json_str)

                # 다시 다음 구간 측정을 위해 초기화
                self.records = []

            # 4. 5초 후 반복
            time.sleep(5)


# 문제 3에서 만든 DummySensor 인스턴스화
ds = DummySensor()

# MissionComputer 인스턴스는 RunComputer라는 이름으로 생성
RunComputer = MissionComputer()

# RunComputer.get_sensor_data(ds)를 호출하여 반복적으로 데이터 수집/출력
RunComputer.get_sensor_data(ds)