#!/usr/bin/env python3
#New file created
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import asyncio
from decimal import Decimal
import os
from dotenv import load_dotenv
load_dotenv()
import AsyncCryptoV1
#import credentials
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

#create an instance of the client
client = AsyncCryptoV1.CryptoLinkClient(api_key, api_secret)


#first load the iris dataset
async def load_data():
    
    iris = await client.get_candles(ticker='KEYCAT-USD')
    return iris

async def train():
    pass

async def scale_features():
    pass

async def create_model():
    pass

async def hyperparameters(param):
    pass



X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

#define the hyperparameter grid
param_grid = {
    'n_estimators': [10, 50, 100],
    'max_depth': [None, 5, 10],
    'min_samples_split':[2, 5, 10]
}

#init the random forest model
rf = RandomForestClassifier(random_state=42)

#perform the grid search
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5)
grid_search.fit(X_train, y_train)

#print the best hyperparameters
print(f"the best hyperparameter is {grid_search.best_params_}")

best_model = grid_search.best_estimator_
accuracy = best_model.score(X_test, y_test)
print(f"the accuraccy is: {accuracy}")




async def test():
    
    
    pass


async def main():
    pass
    
    
    #test = await test()
    
    #print(test)
if __name__=='__main__':
    asyncio.run(main())
    
    