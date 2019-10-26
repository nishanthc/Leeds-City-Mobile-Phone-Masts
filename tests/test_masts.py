from masts import csv_to_dict, ascending_by_current_rent, specific_lease_years, tenant_mast_count, leases_between_dates

masts_data_csv = "tests/test.csv"


def test_ascending_by_current_rent():
    mast_data, columns = csv_to_dict(masts_data_csv)
    sorted_data, tables = ascending_by_current_rent(columns, mast_data)
    ordered_rent = []
    for row in sorted_data:
        ordered_rent.append(float(row["Current Rent"]))
    assert ordered_rent == [0.0, 1.0, 2.0, 3.0, 4.0]


def test_specific_lease_years():
    mast_data, columns = csv_to_dict(masts_data_csv)
    sorted_data, total_rent, tables = specific_lease_years(columns, mast_data)
    specified_lease_masts = []
    for row in sorted_data:
        specified_lease_masts.append((int(row["Units Reference"])))
    assert specified_lease_masts == [6, 10]
    assert total_rent == 11


def test_tenant_mast_count():
    mast_data, columns = csv_to_dict(masts_data_csv)
    dictionaries, tables = tenant_mast_count(mast_data)
    assert dictionaries[0]["CTIL (Vodafone/O2/T Mobile) Cornerstone Telecommunications Infrastructure Ltd"] == 5

def test_leases_between_dates():
    mast_data, columns = csv_to_dict(masts_data_csv)
    sorted_data, tables = leases_between_dates(columns, mast_data)
    assert int(sorted_data[0]["Units Reference"]) == 10

