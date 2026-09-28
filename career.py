import sqlite3
import os 
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add-skill")
add_parser.add_argument("--skill_name", required=True)
add_parser.add_argument("--skilled", default="1")
add_parser.add_argument("--skill_category", default="data-engineer")
add_parser.add_argument("--skill_level", default="Intermediate")

add_cert_parser = subparsers.add_parser("add-cert")
add_cert_parser.add_argument("--cert_name", required=True)
add_cert_parser.add_argument("--cert_organization", required=True)
add_cert_parser.add_argument("--status", default="completed")
add_cert_parser.add_argument("--cert_category", default="data-engineer")

add_job_parser = subparsers.add_parser("add-job")
add_job_parser.add_argument("--company_name", required=True)
add_job_parser.add_argument("--job_title", required=True)
add_job_parser.add_argument("--job_location", default="Pune")

fetch_parser = subparsers.add_parser("fetch-skills")
fetch_cert_parser = subparsers.add_parser("fetch-certs")
fetch_job_parser = subparsers.add_parser("fetch-jobs")

delete_parser = subparsers.add_parser("delete-skill")
delete_parser.add_argument("--skill_name", required=True)

update_parser = subparsers.add_parser("update-skill")
update_parser.add_argument("--skill_name", required=True)
update_parser.add_argument("--skilled", default="1")
update_parser.add_argument("--skill_category", default="data-engineer")
update_parser.add_argument("--skill_level", default="Intermediate")



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


def create_table(create_table_sql, conn=None):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cur = conn.cursor()
        print("executing create_table_sql")
        cur.executescript(create_table_sql)
        conn.commit()
        cur.close()
    except sqlite3.Error as e:
        print(e)

def add_skill(skill_name, conn=None, skilled="1", skill_category='data-engineer', skill_level='Intermediate'):
    try:
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

def add_cert(cert_name, conn=None, cert_organization="Microsoft", status="completed", cert_category="data-engineer"):
    try:
        cur = conn.cursor()
        print(f"adding cert: {cert_name} with organization: {cert_organization}, status: {status}, category: {cert_category}")
        cur.execute("""
            INSERT INTO certifications (cert_name, cert_organization, status, cert_category)
            VALUES (?, ?, ?, ?)
        """, (cert_name, cert_organization, status, cert_category))
        conn.commit()
        cur.close()
    except sqlite3.Error as e:
        print(e)


def add_job(company_name, conn=None, job_title="Data Engineer", job_location="Pune"):
    try:
        cur = conn.cursor()
        print(f"adding job: {job_title} at {company_name} in {job_location}")
        cur.execute("""
            INSERT INTO applied_jobs (company_name, job_title, job_location)
            VALUES (?, ?, ?)
        """, (company_name, job_title, job_location))
        conn.commit()
        cur.close()
    except sqlite3.Error as e:
        print(e)


def delete_skill(skill_name, conn=None):
    try:
        cur = conn.cursor()
        print(f"deleting skill: {skill_name}")
        cur.execute("DELETE FROM skills WHERE skill_name = ?", (skill_name,))
        conn.commit()
        cur.close()
    except sqlite3.Error as e:
        print(e)

def fetch_skills(conn=None):
    try:
        cur = conn.cursor()
        print("fetching skills")
        cur.execute("SELECT * FROM certifications")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except sqlite3.Error as e:
        print(e)

def fetch_certs(conn=None):
    try:
        cur = conn.cursor()
        print("fetching certs...")
        cur.execute("SELECT * FROM certifications")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except sqlite3.Error as e:
        print(e)

def fetch_jobs(conn=None):
    try:
        cur = conn.cursor()
        print("fetching jobs...")
        cur.execute("SELECT * FROM applied_jobs")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(path, 'schema.sql')
    conn = create_connection("career.db")

    with open(sql_file, 'r') as f:
        create_table_sql = f.read()
    create_table(create_table_sql, conn)
    
    args = parser.parse_args()
    
    if args.command == "add-skill":
        add_skill(args.skill_name, conn, args.skilled, args.skill_category, args.skill_level)
    elif args.command == "fetch-skills":
        fetch_skills(conn)
    elif args.command == "delete-skill":
        delete_skill(args.skill_name, conn)
    elif args.command == "update-skill":
        delete_skill(args.skill_name, conn)
        add_skill(args.skill_name, conn, args.skilled, args.skill_category, args.skill_level)
    elif args.command == "add-cert":
        add_cert(args.cert_name, conn, args.cert_organization, args.status, args.cert_category)
    elif args.command == "fetch-certs":
        fetch_certs(conn)
    elif args.command == "add-job":
        add_job(args.company_name, conn, args.job_title, args.job_location)
    elif args.command == "fetch-jobs":
        fetch_jobs(conn)
    else:
        parser.print_help()

    conn.close()