# vuln_searchor.py
def dangerous_search(engine, query):
    # ❌ Vulnerable: eval() is applied directly to user input
    return eval(f"Engine.{engine}.search('{query}')")

if __name__ == "__main__":
    # Simulating attacker input:
    engine = "__import__('os').system('echo injected') or safe"
    dangerous_search(engine, "test")
