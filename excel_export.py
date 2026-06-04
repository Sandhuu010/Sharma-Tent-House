from openpyxl import Workbook
import os


def export_to_excel(file_name, data1, data2=None):

    """
    Supports 2 formats:
    1. export_to_excel(file, rows_dict)
    2. export_to_excel(file, headers, rows_list)
    """

    if not data1:
        print("No data found.")
        return

    workbook = Workbook()
    sheet = workbook.active

    # CASE 1: only rows passed (list of dicts)
    if data2 is None:

        rows = data1

        headers = list(rows[0].keys())

        sheet.append(headers)

        for row in rows:
            sheet.append(list(row.values()))

    # CASE 2: headers + rows passed
    else:

        headers = data1
        rows = data2

        sheet.append(headers)

        for row in rows:
            sheet.append(row)

    try:
        workbook.save(file_name)
        print(f"\nExcel file created: {file_name}")

        try:
            os.startfile(file_name)
        except Exception:
            print("File created but could not open automatically.")

    except PermissionError:
        print(f"\nClose '{file_name}' if it is open in Excel and try again.")

    except Exception as e:
        print(f"\nExcel export failed: {e}")