import pandas as pd
import numpy as np
import sys
import streamlit as st


number_of_games = st.sidebar.number_input('number of events', min_value=2)
lay_commission = st.sidebar.number_input('lay commission', min_value=0)
fta_odds = st.sidebar.number_input('FTA odds', min_value=1)
back_odds = st.sidebar.number_input('back odds', min_value=0.01)
back_stake = st.sidebar.number_input('back stake', min_value=1)
lay_odds = st.sidebar.number_input('lay odds', min_value=0.001)
lay_stake = st.sidebar.number_input('lay stake', min_value=1)

back_win_amount = np.round((back_odds - 1) * back_stake, 2)
lay_win_amount = np.round(lay_stake * (1.0 - lay_commission), 2)
lay_liability = np.round((lay_odds - 1) * lay_stake, 2)
back_win_ql = np.round(abs(back_win_amount - lay_liability), 2)
lay_win_ql = np.round(abs(lay_win_amount - back_stake), 2)

avg_ql = (back_win_ql + lay_win_ql) / 2
fta_amount = back_win_amount + lay_win_amount


st.title('2UPs')

st.text(f"Back Win: {back_win_amount}\nLay Win: {lay_win_amount}\nLay Liability: {lay_liability}\nBack QL: {back_win_ql}\nLay QL: {lay_win_ql}\nFTA win: {fta_amount}")


# p = 1 / fta_odds
st.text('{}'.format(fta_odds))

win_sums = []
loss_sums = []
non_fta = 0
fta = 0

for t in range(number_of_games):
    if t % 10000 == 0:
        print(".", end='', flush=True)
    outcome = np.random.randint(1, fta_odds + 1)
    if outcome == 1:
        win_sums.append(fta_amount)
        loss_sums.append(0)
        fta += 1
    else:
        loss_sums.append(avg_ql)
        win_sums.append(0)
        non_fta += 1

pct_non_fta = (non_fta / number_of_games) * 100
pct_fta = (fta / number_of_games) * 100


data = pd.DataFrame({'win_sums' : win_sums, 'loss_sums' : loss_sums})
data['profitable'] = data.win_sums > data.loss_sums
st.text("\n\nNon FTA games %: {}\nFTA games %: {}\n".format((non_fta/number_of_games)*100, ((fta/number_of_games)*100)))
st.text("Average win : {}\nAverage loss: {}\nAverage profit: {}".format(data.win_sums.mean(), data.loss_sums.mean(), data.win_sums.mean() - data.loss_sums.mean()))
