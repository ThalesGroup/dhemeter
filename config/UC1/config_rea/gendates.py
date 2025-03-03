# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import datetime
import json

start_date = datetime.datetime(2023, 5, 29, 10, 0, 0)
end_date = datetime.datetime(2024, 6, 29, 10, 0, 0)

date_list = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days + 1)]

# isoformat like 2023-05-29T00:00:00.000Z
formatted_dates = [date.strftime('%Y-%m-%dT%H:%M:%S.000Z') for date in date_list]

data = {"reanalysis-time": formatted_dates}

with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)
