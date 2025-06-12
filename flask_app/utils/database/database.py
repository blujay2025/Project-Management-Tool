import mysql.connector
import hashlib
from math import pow

class database:
    # Initialize database configurations
    def __init__(self, purge=False):
        self.database = 'db'
        self.host = '127.0.0.1'
        self.user = 'master'
        self.port = 3306
        self.password = 'master'
        self.tables = ['users', 'projects', 'cards']
        self.encryption = {'oneway': {'salt': b'pmtergrlgnfgucmbhdyiuczzjhvcyrrdtlmxphvnwizh',
                                      'n': int(pow(2, 5)),
                                      'r': 9,
                                      'p': 1
                                      }
                           }

    # Queries the database given a set of parameters
    def query(self, query="SELECT * FROM users", parameters=None):

        cnx = mysql.connector.connect(host=self.host,
                                      user=self.user,
                                      password=self.password,
                                      port=self.port,
                                      database=self.database,
                                      charset='latin1'
                                      )

        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    # Creates the tables at the instantiation of the app
    def createTables(self, purge=False, data_path='flask_app/database/'):
        if purge == True:
            self.query("DROP TABLE IF EXISTS users;")
            self.query("DROP TABLE IF EXISTS projects;")
            self.query("DROP TABLE IF EXISTS cards;")

        sql_files_list = ['/create_tables/users.sql', '/create_tables/projects.sql',
                          '/create_tables/cards.sql']
        for sql_file in sql_files_list:
            complete_data_path = data_path + sql_file
            with open(complete_data_path, 'r') as complete_sql_file:
                retrieved_sql_query = complete_sql_file.read()
                self.query(retrieved_sql_query)

    # Insert rows into the database using the query function
    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        modified_parameters = []
        for value in parameters:
            modified_parameters.append(value[0])

        # insertRows takes in table name, columns, and parameters and extracts the relevant information to use in an insert SQL query to fill SQL tables
        sql_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})"
        row = self.query(sql_query, modified_parameters)
        return row[0]['LAST_INSERT_ID()']

    
    #######################################################################################
    # AUTHENTICATION RELATED
    #######################################################################################

    # Provides oneway Encryption
    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt=self.encryption['oneway']['salt'],
                                          n=self.encryption['oneway']['n'],
                                          r=self.encryption['oneway']['r'],
                                          p=self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string
    

    # Authenticates if valid user or not
    def authenticate(self, email='me@email.com', password='password'):
        user_info = self.query(
            "SELECT * FROM users WHERE email = %s", (email,))
        if not user_info:
            return {'success': 0}

        stored_password = user_info[0]['password']
        encrypted_input_password = self.onewayEncrypt(password)
        if not encrypted_input_password == stored_password:
            return {'success': 0}

        return {'success': 1}