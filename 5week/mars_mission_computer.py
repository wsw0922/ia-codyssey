import os
import platform
import subprocess

class MissionComputer:
    def __init__(self):
        pass

    # Linux 전용
    def _get_meminfo_linux(self):
        info = {}
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        info['MemTotal'] = float(line.split()[1])
                    elif line.startswith('MemAvailable:'):
                        info['MemAvailable'] = float(line.split()[1])
        except:
            pass
        return info
    
    # mac 전용
    def _get_meminfo_darwin(self):
        try:
            output = subprocess.check_output(['sysctl', '-n', 'hw.memsize'])
            total_bytes = int(output.strip())
            total_mb = total_bytes / (1024 * 1024)
            return total_mb
        except Exception:
            return None

    def get_mission_computer_info(self):
        # OS/버전/CPU/메모리 정보
        os_name = platform.system()
        os_version = platform.version()
        cpu_type = platform.processor()
        cpu_cores = os.cpu_count() or 1

        if os_name == 'Linux':
            meminfo = self._get_meminfo_linux()
            if 'MemTotal' in meminfo:
                mem_gb = f"{meminfo['MemTotal'] / (1024 * 1024):.2f}"
        elif os_name == 'Darwin':  # macOS
            mem_mb = self._get_meminfo_darwin()
            if mem_mb:
                mem_gb = f"{mem_mb / 1024:.2f}"  # MB -> GB

        data = {
            'os_name': os_name,
            'os_version': os_version,
            'cpu_type': cpu_type,
            'cpu_cores': cpu_cores,
            'memory_size_gb': mem_gb
        }

        # 콘솔에도 출력
        print('[MissionComputer Info]', data, sep='\n')
        # 딕셔너리 그대로 반환
        return data

    def get_mission_computer_load(self):
        # CPU/메모리 사용률
        cpu_usage = None
        mem_usage = None
        os_name = platform.system()

        if os_name in ('Linux', 'Darwin'):
            # CPU 사용률: 1분 loadavg / 코어수 * 100% 근사
            try:
                load1, _, _ = os.getloadavg()
                cores = os.cpu_count() or 1
                cpu_usage = (load1 / cores) * 100
            except:
                pass

            # 메모리 사용률: (MemTotal - MemAvailable) / MemTotal * 100
            meminfo = self.get_mission_computer_info()
            if 'MemTotal' in meminfo and 'MemAvailable' in meminfo:
                used = meminfo['MemTotal'] - meminfo['MemAvailable']
                mem_usage = (used / meminfo['MemTotal']) * 100

        # Windows 등에서 실패 시 기본값
        if cpu_usage is None:
            cpu_usage = 50.0
        if mem_usage is None:
            mem_usage = 40.0

        data = {
            'cpu_usage_percent': round(cpu_usage, 2),
            'memory_usage_percent': round(mem_usage, 2)
        }

        # 콘솔에도 출력
        print('[MissionComputer Load]', data, sep='\n')
        # 딕셔너리 그대로 반환
        return data


if __name__ == '__main__':
    runComputer = MissionComputer()
    
    # 1) 콘솔에 출력 + 2) 데이터 반환
    info_data = runComputer.get_mission_computer_info()
    load_data = runComputer.get_mission_computer_load()

    # 반환값을 settings.txt에 저장
    with open('settings.txt', 'w') as f:
        f.write('[MissionComputer Info]\n')
        f.write(str(info_data) + '\n\n')
        f.write('[MissionComputer Load]\n')
        f.write(str(load_data) + '\n')