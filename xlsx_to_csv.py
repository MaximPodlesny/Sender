import pandas as pd

read_file = pd.read_excel('sokalslaya-all.xlsx')

read_file.to_csv('sokalskaya-all.csv', index = False, header = True)