# vuln_mindsdb.py
def insert_metadata(metadata_value):
    # ❌ Vulnerable: passing unsanitized metadata through eval
    result = eval(metadata_value)
    store_to_db({'metadata': result})
