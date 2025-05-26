import sqlite3

def save_df_to_db(detail_name, df, db_path):
    con = sqlite3.connect(db_path)
    df.to_sql(detail_name, con, if_exists="append", index=False)
    con.close()