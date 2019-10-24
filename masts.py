import csv

def csv_to_dict():
    csv_dictionary = csv.DictReader(open("data/mobile_phone_masts.csv"))
    return csv_dictionary


def ascending_by_current_rent(mast_data):
    csv_dict = sorted(mast_data, key=lambda row: float(row['Current Rent']))
    for row in csv_dict:
        print(row)


# mast_data = csv_to_dict()
#
# print(ascending_by_current_rent(mast_data))
