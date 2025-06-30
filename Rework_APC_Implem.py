import sqlite3
import login_menu

def main():
    cx = sqlite3.connect("assignment3.db")
    cursor = cx.cursor()
    login_menu.login(cursor, cx)
    cx.commit()
    cx.close()

if __name__ == "__main__":
    main()
