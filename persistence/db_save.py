import sqlite3
from details_parsing.details_info import detail_id_names

def update_details_in_db(db_path, detail_dfs):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for detail, df in detail_dfs.items():
        cursor.execute(f"DELETE FROM {detail}")

        existing_models = set(
            row[0] for row in cursor.execute(f"SELECT model FROM {detail}").fetchall()
        )

        insertable_df = df[~df['model'].isin(existing_models)]
        if not insertable_df.empty:
            placeholders = ", ".join(["?"] * len(insertable_df.columns))
            insert_query = f"INSERT INTO {detail} ({', '.join(insertable_df.columns)}) VALUES ({placeholders})"
            cursor.executemany(insert_query, insertable_df.itertuples(index=False, name=None))

        print(f"{len(insertable_df)} new rows inserted into '{detail}'.")

    conn.commit()
    conn.close()

def insert_distributor_info(db_path, distributor_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for model, df in distributor_data.items():
        id_value = None
        id_name = None

        for detail, id_column_name in detail_id_names.items():
            try:
                cursor.execute(f"SELECT {detail.lower()}_id FROM {detail} WHERE model = ?", (model,))
                result = cursor.fetchone()
                if result:
                    id_value = result[0]
                    id_name = id_column_name
                    break
            except sqlite3.Error as e:
                print(f"Error querying model '{model}' in table '{detail}': {e}")

        if id_value is None or id_name is None:
            print(f"Skipping distributor info for model '{model}': model not found in any table.")
            continue

        for _, row in df.iterrows():
            insert_data = {
                'distributor_name': row['distributor_name'],
                'distributor_link': row['distributor_link'],
                'price': row['price'],
                'is_available': row['is_available'],
                'frame_id': None,
                'propeller_id': None,
                'camera_id': None,
                'vtx_id': None,
                'rx_id': None,
                'antenna_id': None,
                'battery_id': None,
                'motor_id': None,
                'stack_id': None
            }
            insert_data[id_name] = id_value

            columns = ", ".join(insert_data.keys())
            placeholders = ", ".join(["?"] * len(insert_data))
            values = tuple(insert_data.values())
            try:
                cursor.execute(f"INSERT INTO Distributor ({columns}) VALUES ({placeholders})", values)
            except sqlite3.IntegrityError as e:
                print(f"Integrity error inserting distributor data for model '{model}': {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    conn.commit()
    conn.close()