import sqlite3
import os 
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add")
add_parser.add_argument("--skill_name", required=True)
add_parser.add_argument("--skilled", type=int, default=0)
add_parser.add_argument("--skill_category", default="data-engineer")
add_parser.add_argument("--skill_level", default="Intermediate")


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        print(f"creating connection to {db_file}")
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        conn = create_connection("career.db")
        cur = conn.cursor()
        print("executing create_table_sql")
        cur.execute(create_table_sql)
        cur.execute("""
            INSERT INTO skills VALUES
            (2,'t-sql',1,'data-engineer', 'Intermediate')
        """)
        conn.commit()
        cur.execute("SELECT * FROM skills")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except sqlite3.Error as e:
        print(e)

def add_skill(skill_name, skilled=0, skill_category='data-engineer', skill_level='Intermediate'):
    try:
        conn = create_connection("career.db")
        cur = conn.cursor()
        print(f"adding skill: {skill_name} with skilled: {skilled}, category: {skill_category}, level: {skill_level}")
        cur.execute("""
            INSERT INTO skills (skill_name, skilled, skill_category, skill_level)
            VALUES (?, ?, ?, ?)
        """, (skill_name, skilled, skill_category, skill_level))
        conn.commit()
        cur.close()
    except sqlite3.Error as e:
        print(e)

def fetch_skills():
    try:
        conn = create_connection("career.db")
        cur = conn.cursor()
        print("fetching skills")
        cur.execute("SELECT * FROM skills")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    #fetch_skills()
    path = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(path, 'schema.sql')
    with open(sql_file, 'r') as f:
        # print("reading schema.sql")
        # print(f"sql_file content: {f.read()}")
        create_table_sql = f.read()
    #create_table(create_table_sql)
    args = parser.parse_args()
    if args.command == "add":
        add_skill(args.skill_name, args.skilled, args.skill_category, args.skill_level)