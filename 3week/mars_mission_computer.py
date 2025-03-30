import random

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
        log = (
            "Logged Data - "
            f"내부 온도: {self.env_values['mars_base_internal_temperature']:.2f}°C, "
            f"외부 온도: {self.env_values['mars_base_external_temperature']:.2f}°C, "
            f"내부 습도: {self.env_values['mars_base_internal_humidity']:.2f}%, "
            f"외부 광량: {self.env_values['mars_base_external_illuminance']:.2f} W/m2, "
            f"내부 CO2 농도: {self.env_values['mars_base_internal_co2']:.4f}%, "
            f"내부 산소 농도: {self.env_values['mars_base_internal_oxygen']:.2f}%"
        )

        with open('log.txt', 'a') as file:
            file.write(log + '\n')

        return self.env_values


# 인스턴스 생성 및 테스트
ds = DummySensor()
ds.set_env()
env = ds.get_env()

print(env)