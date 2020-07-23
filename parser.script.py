# sheet.cell_value(2 192'ye kadar, 0'dan 12'ye kadar)


import xlrd
loc = ("medicine_list.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


for row in range(2, 193):
    array = []
    for column in range(0, 13):
        if column == 5:
            continue
        value = sheet.cell_value(row, column)
        if column == 0:
            value = int(value)
        array.append(value)
    medicine = Medicines.objects.create(
        item_no = array[0],
        importer = array[1],
        chemical = array[2],
        generic = array[3],
        profile = array[4],
        item_type = array[5],
        measure = array[6] ,
        formulation = array[9],
        route = array[10],
        pbb_code = array[11]
    )
    medicine.save()