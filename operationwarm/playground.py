import pandas as pd

myseries = pd.Series([1,5,0,7,5], index=[0,1,2,3,4])

print(myseries[myseries == 5].index.tolist())
