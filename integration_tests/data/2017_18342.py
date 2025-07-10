# vulnerable_py.py
import yaml

def load_yaml(data):
    # ❌ unsafe: yaml.load defaults to the Full Loader
    return yaml.load(data)

if __name__ == "__main__":
    unsafe_yaml = """
    !!python/object/apply:os.system ["echo 'Hello from vulnerable code'"]
    """
    result = load_yaml(unsafe_yaml)
    print("Result:", result)
