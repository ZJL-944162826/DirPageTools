from openpyxl import Workbook


def write_list(work_sheet, row):
    work_sheet.append(row)


if __name__ == '__main__':
    wb = Workbook()
    print(wb.sheetnames)
    sheet = wb.active
    print(sheet.title)
    wb.save('char_excel_text.xlsx')

