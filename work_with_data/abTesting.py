import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import requests
import random
# df_ab_test = pd.read_csv('summary.csv')
# print(df_ab_test.head())
# print(df_ab_test.describe())
# print(df_ab_test.groupby("goal").sum())

# sns.set_theme()
# tips = pd.read_csv('summary.csv')

# # sns.relplot(
# #     data=tips, kind='line',
# #     x='age', y='positon', col='goal',
# #     hue='age', style='age', size='age'
# # )
# # sns.lmplot(data=tips, x='height', y='weight', col='age', hue='positon')
# sns.displot(data=tips, x="age", col="goal", kde=True)
# plt.show()

# The multi-armed bandit problem is to design a sequence of actions, 
# that will maximize the expected total reward over some time period. 
# The problem is to design a sequence of actions 
# (what slot machines to play at certain time step) 
# in order to maximize the total expected reward over 
# a certain time period. Gambler need to figure out how 
# to play 3 machines such that he maximizes the sum of rewards over a time period.
a = [65, 41, 27]
b = [52,35,18]
print(a is b)