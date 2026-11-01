import sys

def environment_info():
    return {"python_major": sys.version_info.major, "executable": sys.executable,
            "is_venv": sys.prefix != sys.base_prefix}

if __name__ == "__main__":
    info = environment_info()
    for key, value in info.items():
        print(f"{key}: {value}")
