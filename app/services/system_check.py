import shutil
import psutil


def check_system_status():
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("/")

    return {
        "memory": {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "percent": memory.percent
        },
        "disk": {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "percent": round((disk.used / disk.total) * 100, 2)
        }
    }