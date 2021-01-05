import pandas as pd
import numpy as np

IN_FILE = "nasdaq_screener.csv"
OUT_FILE = "portfolio.csv"
IND_SIZE = 300
PORT_SIZE = 100000

#Setup
data = pd.read_csv(IN_FILE)
data.rename(columns ={'Last Sale':'Price', 'Market Cap':'Market_Cap'}, inplace=True)
data["Price"] = data["Price"].transform(lambda x: float(x[1:]))
data.sort_values("Market_Cap", ascending = False, inplace = True)
data = data[["Symbol","Price","Market_Cap"]].iloc[:IND_SIZE].reset_index(drop = True)

#Basic attributes
data["Weight"] = data["Market_Cap"]/data["Market_Cap"].sum()
data["Ideal_Alloc"] = data["Weight"] * PORT_SIZE

#Webster/Sainte-Laguë method
num_stocks = pd.Series(np.zeros(len(data)))
while num_stocks.dot(data["Price"])<PORT_SIZE:
        quot = (data["Weight"]/data["Price"])/(2*num_stocks+1)
        stck = quot.idxmax()
        num_stocks[stck] += 1

#Set results
data["Num_Stocks"] = num_stocks
data["Port_Alloc"] = data["Num_Stocks"] * data["Price"]
data["Port_Weight"] = data["Port_Alloc"]/data["Port_Alloc"].sum()
data["Final_Diff"] = data["Ideal_Alloc"] - data["Port_Alloc"]

data.to_csv(OUT_FILE)

#print(abs(data.Weight-data.Port_Weight).sum()/2)

#print(data.iloc[data.Final_Diff.abs().nlargest(20).index])

