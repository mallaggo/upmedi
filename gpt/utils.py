def convert_to_excel_table(data):

    if not data:
        return [], []

    headers = list(data[0].keys())

    rows = []

    for item in data:
        rows.append(
            [item.get(key) for key in headers]
        )

    return headers, rows