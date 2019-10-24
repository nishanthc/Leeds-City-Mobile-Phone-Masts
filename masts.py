import csv

import inquirer
from terminaltables import AsciiTable


def csv_to_dict():
    csv_dictionary = csv.DictReader(open("data/mobile_phone_masts.csv"))
    return csv_dictionary, csv_dictionary.fieldnames


def ascending_by_current_rent(columns, mast_data):
    sorted_data = list(sorted(mast_data, key=lambda row: float(row['Current Rent']))[:5])
    display_table(columns, sorted_data)


def specific_lease_years(columns, mast_data):
    mast_data = list(mast_data)
    sorted_data = []
    for n, row in enumerate(mast_data):
        try:
            if int(row["Lease Years"]) == 25:
                sorted_data.append(row)
        except ValueError:
            pass
    display_table(columns, sorted_data)
    # List Comprehension
    total_rent = sum([(int(item["Current Rent"])) for item in sorted_data])
    print(f"Total Rent: {total_rent}")


def display_table(columns, sorted_data):
    data_list = []
    for ordered_dictionary in sorted_data:
        row_list = []
        for key, value in ordered_dictionary.items():
            row_list.append(value)
        data_list.append(row_list)
    table_data = [columns]
    table_data.extend(data_list)
    table = AsciiTable(table_data)
    print(table.table)


def execute_operation(answers):
    mast_data, columns = csv_to_dict()
    if answers["operation"] == "First 5 masts sorted by Current Rent in ascending order":
        ascending_by_current_rent(columns, mast_data)
    elif answers["operation"] == "Masts with a 25 year lease and their total rent":
        specific_lease_years(columns, mast_data)


questions = [
    inquirer.List('operation',
                  message="Which operation would you like to run?",
                  choices=[
                      'First 5 masts sorted by Current Rent in ascending order',
                      'Masts with a 25 year lease and their total rent',
                      'Standard',
                      'Medium',
                      'Small',
                      'Micro'
                  ],
                  ),
]
answers = inquirer.prompt(questions)
execute_operation(answers)
