import numpy as np
import pandas as pd

my_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,11,10,9,8,7,6,5,4,3,2,1]
repeated_list = my_list * 10
df = pd.DataFrame(repeated_list, columns=['Load_synthetic'])
df.to_csv('wecc_load.csv', index=False)
print(df)