import os
import re
import sqlite3 

SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'watchdog.db')

class Database:
    def __init__(self):
        self.con = sqlite3.connect(SQLITE_PATH)

    def execute(self, sql, parameters=[]):
        c = self.con.cursor()
        c.execute(sql, parameters)
        self.con.commit()
    
    def select(self, sql, parameters=[]):
        c = self.con.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def userSignUp(self,name,email,username,password):
        self.execute('INSERT INTO user (name,email,username,password) VALUES (?, ?, ?, ?)', [name, email, username, password])
    
    def expense(self,description,category,amount,username):
        self.execute('INSERT INTO expense (username,description,category,amount) VALUES (?, ?, ?, ?)', [username,description,category,amount])

    def add_account(self,account,balance,username):
        self.execute('INSERT INTO accounts (username,account,balance) VALUES (?, ?, ?)', [username,account,balance])

    def add_budget(self,category,budget,username):
        self.execute('INSERT INTO budget (username,category,budget) VALUES (?, ?, ?)', [username,category,budget])


    def userLogin(self,username):
        data = self.select('SELECT * FROM user WHERE username=?', [username])
        if data:
            d = data[0]
            return {
                'name': d[0],
                'email': d[1],
                'username': d[2],
                'password': d[3]
                }
        else:
            return None

    def table(self,username):
        data = self.select('SELECT * FROM expense WHERE username=?', [username])
        return [{
            'username' : d[0],
            'description': d[1],
            'category': d[2],
            'amount': d[3],
            } for d in data]

    def budgetCheck(self,username):
        data = self.select('SELECT * FROM budget WHERE username=?', [username])
        return [{
            'username' : d[0],
            'category' : d[1],
            'budget': d[2],
            } for d in data]

    def chart(self,username):
        data = self.select('SELECT category, SUM(amount) as total FROM expense WHERE username=? GROUP BY category', [username])
        return [{
            'category' : d[0],
            'total': d[1],
            } for d in data]

    def changeUser(self,username,name):
        self.execute('UPDATE user SET username=? WHERE username=?', [username, name])
        self.execute('UPDATE expense SET username=? WHERE username=?', [username, name])
        self.execute('UPDATE budget SET username=? WHERE username=?', [username, name])
        self.execute('UPDATE accounts SET username=? WHERE username=?', [username, name])

    def changePwd(self,pwd,name):
        self.execute('UPDATE user SET password=? WHERE username=?', [pwd, name])
    
    def close(self):
        self.con.close()





