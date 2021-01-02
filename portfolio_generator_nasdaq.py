import pandas as pd
import numpy as np

IN_FILE = "nasdaq_screener.csv"
OUT_FILE = "portfolio.csv"
IND_SIZE = 300
PORT_SIZE = 100000
BAD_COUNTRIES = "China,Belgium,India,France,Hong Kong,Brazil,Argentina,\
Spain,Mexico,Italy,Bermuda,Colombia,Cayman Islands,Indonesia,Jersey,Peru"
SEED = "08bfaa9472b48ebc93172977d129767b9ddcbe85217308fef73471fd17f37b51"

#Setup
data = pd.read_csv(IN_FILE)
data.rename(columns ={'Last Sale':'Price', 'Market Cap':'Market_Cap'}, inplace=True)
data["Price"] = data["Price"].transform(lambda x: float(x[1:]))
data.sort_values("Market_Cap", ascending = False, inplace = True)
#data = data[~data.Country.isin(BAD_COUNTRIES.split(','))]
data = data[["Symbol","Price","Market_Cap"]].iloc[:IND_SIZE].reset_index(drop = True)

#Basic attributes
data["Weight"] = data["Market_Cap"]/data["Market_Cap"].sum()
data["Ideal_Alloc"] = data["Weight"] * PORT_SIZE

#May choose floor allocation as a starting point
#data["Floor_Alloc"] = data["Ideal_Alloc"]-data["Ideal_Alloc"]%data["Price"]
#data["Floor_Num_Stocks"] = data["Floor_Alloc"]/data["Price"]
#data["Shortage"] = data["Ideal_Alloc"] - data["Floor_Alloc"]
#
#num_stocks = data["Floor_Num_Stocks"].copy()
#diff = data["Shortage"].copy()

#Distribute surplus (last buy will result a margin loan)
num_stocks = pd.Series(np.zeros(len(data)))
diff = data["Ideal_Alloc"].copy()
pos_diff = diff
#bg = np.random.PCG64(int(SEED[:32],16))
while diff.sum() > 0:
        stck = pos_diff.sample(weights = pos_diff/data["Price"]).index[0]
        #random_state = bg
        num_stocks[stck] += 1
        diff.iloc[stck] -= data.iloc[stck]["Price"]
        pos_diff = diff.transform(lambda x: max(x,0))

#Set results
data["Num_Stocks"] = num_stocks
data["Port_Alloc"] = data["Num_Stocks"] * data["Price"]
data["Port_Weight"] = data["Port_Alloc"]/data["Port_Alloc"].sum()
data["Final_Diff"] = data["Ideal_Alloc"] - data["Port_Alloc"]

data.to_csv(OUT_FILE)

#print(abs(data.Weight-data.Port_Weight).sum()/2)

#print(data.iloc[data.Final_Diff.abs().nlargest(20).index])

##vals = []
##for cnt in data.Country.unique():
##	#print("{0}:{1}".format(cnt,data[data.Country == cnt]['Market_Cap'].sum()/data['Market_Cap'].sum()))
##        vals.append(data[data.Country == cnt]['Market_Cap'].sum()/data['Market_Cap'].sum())
##df = pd.DataFrame(data={'Country':data.Country.unique(), 'Percent':vals})
##df.sort_values("Percent", ascending = False, inplace = True)
##print(df)

