# 用來清除千位分隔符($和%手動去除了)
import pandas as pd

# 讀取原始 CSV 文件
df = pd.read_csv('Which_country_fits_me/dataset/world-data-2023.csv', thousands=',')

# 輸出乾淨的 CSV
df.to_csv("world-data-2023_cleaned.csv", index=False)