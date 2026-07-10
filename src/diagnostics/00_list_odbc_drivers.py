import pyodbc


def main():
    print("Installed ODBC drivers:")
    print("-" * 40)

    for driver in pyodbc.drivers():
        print(driver)


if __name__ == "__main__":
    main()