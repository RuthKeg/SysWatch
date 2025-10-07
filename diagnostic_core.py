import platform
import psutil
import datetime

def get_system_info():
    info = {
        "Système d’exploitation": platform.system(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
        "Processeur": platform.processor(),
        "Cœurs logiques": psutil.cpu_count(logical=True),
        "Cœurs physiques": psutil.cpu_count(logical=False),
        "RAM totale (Go)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "RAM utilisée (Go)": round(psutil.virtual_memory().used / (1024 ** 3), 2),
        "Espace disque total (Go)": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "Espace disque libre (Go)": round(psutil.disk_usage('/').free / (1024 ** 3), 2),
        "Date du diagnostic": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return info
