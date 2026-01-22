# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import datetime
import json

start_date = datetime.datetime(2023, 5, 29, 10, 0, 0)
end_date = datetime.datetime(2023, 6, 29, 10, 0, 0)

# Générer les dates toutes les heures
delta = datetime.timedelta(hours=1)
date_list = []
current = start_date
while current <= end_date:
    date_list.append(current)
    current += delta

# Format ISO 8601 : 2023-05-29T10:00:00.000Z
formatted_dates = [date.strftime('%Y-%m-%dT%H:%M:%S.000Z') for date in date_list]

data = {"reanalysis-time": formatted_dates}

with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)
