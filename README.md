# Use Case
The Grafana API for alerting is in a state of flux and it is not currently
capable of supporting 

1. Export existing Grafana Managed Alerts from Grafana A
2. Import Grafana Managed Alerts to Grafana B

It is possible to export via a db migration script but there are a few caveats

1. dashboardUid folderUid must be identical in Grafana A and Grafana B. 
2. datasources must be identical in Grafana A and Grafana B.

If Grafana provisioning was used to migrate dashboards and folders from Grafana A to
Grafana B, then all you need to do is export/import the contents of the ```alert_rule```
table. This script is has been tested with Grafana 9.3.0. This script will be obsolete
when Grafana 9.4.0 ships and Grafana 9.4.0-beta has better support for alert rule export/import.

## Quick start

### Step 1
Make sure your python environment has [requirements.txt](./requirements.txt) dependencies installed.
This script was tested with Python 3.10 and probably won't run on Python 2.x.

### Step 2

Create a .env file that has your import/export DB connection credentials. This script
uses postgres but it can support mysql or sqllite, may require adding db package to python 
environment.

```
import_db_connect_string=postgresql://[username:password]@localhost:5432/grafanaA
export_db_connect_string=postgresql://[username:password]@localhost:5432/grafanaB
```

### Step 3

Create [dashboards.yaml](./provisioning/dashboards/dashboards.yaml) entries for all folders that contain alerts you would
like to migrate.

### Step 4 

Make sure Grafana A and Grafana B have the same datasource instances. The following
items need to be the same in both servers:

* name
* type
* uid

### Step 5

Run [alert_migration.py](./alert_migration.py). If there are no errors, then
you should see new alerts in Grafana B. 

```python ./alert_migration.py```

### Troubleshooting

1. *No alerts in Grafana B* - If there is a folder or datasource definition mismatch then you will see WARN messages in the grafana logs.
2. *SQL errors* - The script will either migrate ALL alerts or rollback. Duplicate ```alert_rule``` ids are the most common reason for script failure.