import logging
import os
import csv
from sqlalchemy import create_engine, text, delete, Table, Column, MetaData
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import pandas as pd

handler_stream = logging.StreamHandler()
logging.basicConfig(format='%(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

load_dotenv()
import_db_conn = os.getenv('import_db_connect_string')
export_db_conn = os.getenv('export_db_connect_string')

def export_alerts():
    db = create_engine(import_db_conn)
    with db.begin() as conn:
        sql = text("SELECT * FROM alert_rule;")
        result = conn.execute(sql)
        with open("alert_rule.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in result.cursor.description])  # write headers
            csv_writer.writerows(result.cursor)
        logging.info(f'alert_rule table exported to alert_rule.csv')

def import_alerts():
    alert_rule_df = pd.read_csv('alert_rule.csv')
    db = create_engine(export_db_conn)
    try:
        with db.begin() as conn:
            alert_rule_df.to_sql('alert_rule', con=conn, if_exists='append', index=False)
        logging.info(f'alert_rule imported into grafana db')
    except IntegrityError as ie:
        logging.error(f'alert_rule import error - {ie}')

def delete_alerts(namespace_uid):
    db = create_engine(export_db_conn)
    try:
        with db.begin() as conn:
            metadata_obj = MetaData()
            alert_rule_table = Table(
                "alert_rule",
                metadata_obj,
                Column("namespace_uid")
            )
            stmt = delete(alert_rule_table).where(alert_rule_table.c.namespace_uid == namespace_uid)
            conn.execute(stmt)
        logging.info(f'alert_rule records deleted from grafana db for namespace_uid - {namespace_uid}')
    except IntegrityError as ie:
        logging.error(f'alert_rule import error - {ie}')

if __name__ == "__main__":
    delete_alerts("94Jse01Vz")
    export_alerts()
    import_alerts()
