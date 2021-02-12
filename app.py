import pandas as pd
import numpy as np
import sys
import streamlit as st


number_of_games = st.sidebar.slider('number of events', min_value=10, max_value=10000, value=100, step=1)
lay_commission = st.sidebar.slider('lay commission', min_value=0.0,  max_value=5.0, value=0.0, step=0.1)
fta_odds = st.sidebar.slider('FTA odds', min_value=2, max_value=200, value=60)
back_odds = st.sidebar.number_input('back odds')
back_stake = st.sidebar.number_input('back stake')
lay_odds = st.sidebar.number_input('lay odds')
lay_stake = st.sidebar.number_input('lay stake')

back_win_amount = (back_odds - 1) * back_stake
lay_win_amount = lay_stake * (1.0 - lay_commission)
lay_liability = (lay_odds - 1) * lay_stake 
back_win_ql = abs(back_win_amount - lay_liability)
lay_win_ql = abs(lay_win_amount - back_stake)

avg_ql = (back_win_ql + lay_win_ql) / 2
fta_amount = back_win_amount + lay_win_amount


st.title('2UPs')


st.text("Back Odds: {}\nBack Stake: {}\nLay Odds: {}\nLay Stake:{}\nBack Win: {}\nLay Win: {}\nLay Liability: {}\nBack QL: {}\nLay QL: {}\nFTA win: {}".format(back_odds, back_stake, lay_odds, lay_stake, back_win_amount, lay_win_amount, lay_liability, back_win_ql, lay_win_ql, fta_amount))

win_sums = []
loss_sums = []
non_fta = 0
fta = 0
print("Playing", end='')
for t in range (number_of_games):
    if t % 10000 == 0:
        print(".", end='', flush=True)
    outcome = np.random.randint(1,fta_odds)
    if outcome == 1:
        win_sums.append(fta_amount)
        loss_sums.append(0)
        fta += 1
    else:
        loss_sums.append(avg_ql)
        win_sums.append(0)
        non_fta += 1

data = pd.DataFrame({'win_sums' : win_sums, 'loss_sums' : loss_sums})
data['profitable'] = data.win_sums > data.loss_sums
st.text("\n\nNon FTA games %: {}\nFTA games %: {}\n".format((non_fta/number_of_games)*100, ((fta/number_of_games)*100)))
st.text("Average win : {}\nAverage loss: {}\nAverage profit: {}".format(data.win_sums.mean(), data.loss_sums.mean(), data.win_sums.mean() - data.loss_sums.mean()))
