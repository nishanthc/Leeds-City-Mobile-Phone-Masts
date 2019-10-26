import csv
import datetime
import itertools as it
import os
import sys
import textwrap
from datetime import date
from datetime import datetime
from pprint import pprint

import inquirer
from terminaltables import AsciiTable

masts_data_csv = "data/mobile_phone_masts.csv"


def csv_to_dict(masts_data_csv):
    csv_dictionary = csv.DictReader(open(masts_data_csv))
    return csv_dictionary, csv_dictionary.fieldnames


def ascending_by_current_rent(columns, mast_data):
    sorted_data = list(sorted(mast_data, key=lambda row: float(row['Current Rent']))[:5])
    tables = [display_table(columns, sorted_data)]
    return sorted_data, tables


def specific_lease_years(columns, mast_data):
    mast_data = list(mast_data)
    sorted_data = []
    tables = []
    for n, row in enumerate(mast_data):
        try:
            if int(row["Lease Years"]) == 25:
                sorted_data.append(row)
        except ValueError:
            pass
    tables.append(display_table(columns, sorted_data))
    # List Comprehension
    total_rent = sum([(int(item["Current Rent"])) for item in sorted_data])
    tables.append(display_table(["Total Rent"], [[total_rent]]))
    return sorted_data, total_rent, tables


def tenant_mast_count(mast_data):
    mast_data = list(mast_data)
    tables = []
    keyfunc = lambda row: row['Tenant Name']
    groups_dict = it.groupby(sorted(mast_data, key=keyfunc), keyfunc)
    grouped_dict = {k: sum(1 for a in g) for k, g in groups_dict}
    groups_list = it.groupby(sorted(mast_data, key=keyfunc), keyfunc)
    grouped_list = [[k, sum(1 for a in g)] for k, g in groups_list]
    dictionaries = [grouped_dict]
    columns = ["Tenant Name", "Mast Count"]
    tables.append(display_table(columns, sorted_data=grouped_list))
    return dictionaries, tables


def leases_between_dates(columns, mast_data):
    mast_data = list(mast_data)
    sorted_data = []
    tables = []
    search_start_date_begin = date(1999, 6, 1)
    search_start_date_end = date(2007, 8, 31)

    for n, row in enumerate(mast_data):
        try:
            start_lease_date = datetime.strptime(row["Lease Start Date"], "%d-%b-%y").date()
            end_lease_date = datetime.strptime(row["Lease End Date"], "%d-%b-%y").date()
            next_rent_review = datetime.strptime(row["Next Rent Review"], "%d-%b-%y").date()
            if search_start_date_begin <= start_lease_date <= search_start_date_end:
                row["Lease Start Date"] = start_lease_date.strftime("%d/%m/%Y")
                row["Lease End Date"] = end_lease_date.strftime("%d/%m/%Y")
                row["Next Rent Review"] = next_rent_review.strftime("%d/%m/%Y")

                sorted_data.append(row)
        except ValueError:
            pass
    tables.append(display_table(columns, sorted_data))
    return sorted_data, tables


def display_table(columns, sorted_data):
    data_list = []
    if not sorted_data:
        print("No Results")
    else:
        if not isinstance(sorted_data[0], list):
            for ordered_dictionary in sorted_data:
                row_list = []
                for key, value in ordered_dictionary.items():
                    row_list.append(value)
                data_list.append(row_list)
        table_data = [columns]
        if not isinstance(sorted_data[0], list):
            table_data.extend(data_list)
        else:
            table_data.extend(sorted_data)
        for row in table_data:
            for n, cell in enumerate(row):
                if isinstance(cell, str) and not isinstance(sorted_data[0], list):
                    row[n] = textwrap.shorten(cell, width=18, placeholder="...")
        table = AsciiTable(table_data)
        return table.table


def ask_question():
    questions = [
        inquirer.List('operation',
                      message="Which operation would you like to run?",
                      choices=[
                          'First 5 masts sorted by Current Rent in ascending order',
                          'Masts with a 25 year lease and their total rent',
                          'A dictionary of all tenants with a count of masts they own',
                          'Leases starting between 1st of June 1999 and 31st August 2007',
                      ],
                      ),
    ]
    if sys.stdout.isatty():
        answers = inquirer.prompt(questions)
        os.system('cls' if os.name == 'nt' else 'clear')

        execute_operation(answers)
    else:
        print("Please run this via a terminal")


def execute_operation(answers):
    mast_data, columns = csv_to_dict(masts_data_csv)

    try:
        print(answers["operation"])

        if answers["operation"] == "First 5 masts sorted by Current Rent in ascending order":
            sorted_data, tables = ascending_by_current_rent(columns, mast_data)
        elif answers["operation"] == "Masts with a 25 year lease and their total rent":
            sorted_data, total_rent, tables = specific_lease_years(columns, mast_data)
        elif answers["operation"] == "A dictionary of all tenants with a count of masts they own":
            dictionaries, tables = tenant_mast_count(mast_data)
        elif answers["operation"] == "Leases starting between 1st of June 1999 and 31st August 2007":
            sorted_data, tables = leases_between_dates(columns, mast_data)
        try:
            for dict in dictionaries:
                pprint(dict)
        except NameError:
            pass
        for table in tables:
            print(table)

        ask_question()
    except TypeError:
        # fail graceful
        pass


ask_question()
