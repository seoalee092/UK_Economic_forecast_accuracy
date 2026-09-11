import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

forecasts= pd.read_csv("UK_Economic_project/data/forecasts.csv")
outturns= pd.read_csv('UK_Economic_project/data/outturns.csv')

#print(forecasts.columns. tolist())
#print(outturns.columns.tolist())

#print(forecasts['variable'].unique())
#print(forecasts['forecast_horizon'].unique())
#print(forecasts['frequency'].unique())
#print(forecasts.head(20))

#print(outturns['variable'].unique())
#print(outturns['forecast_horizon'].unique())
#print(outturns.head(20))

gdp_forecasts = forecasts[(forecasts['variable']== "gdpkp") & (forecasts['source']=='mpr') ].copy()
#print(gdp_forecasts.head())
cpi_forecasts = forecasts[(forecasts['variable']== "cpisa") & (forecasts['source']=='mpr')].copy()
#print(cpi_forecasts.head())
gdp_actual = outturns[outturns['variable']== "gdpkp"].copy()
#print(gdp_actual.head())
cpi_actual = outturns[outturns['variable']== "cpisa"].copy()
#print(cpi_actual.head())

for df in [gdp_forecasts, cpi_forecasts, gdp_actual, cpi_actual]:
    df["date"]=pd.to_datetime(df['date'], dayfirst=True)
    df["vintage_date"]=pd.to_datetime(df['vintage_date'], dayfirst=True)

#(wrong) 제일 최근 예측만 남기다 보니 다 코앞 예측만 남음. .groupby('date').last() 는 각 날짜마다 가장 나중에 나온 발표의 예측값만 쓰게함 - 다음분기 데이터로 저번 분기일을 추정한셈. "내일 날씨 맞히기 대회"애서 오늘 아침에 어제 날씨가 어땠는지 추정하기를 한 셈
#Since only leave the latest predictions, all forecasts are from the very near future. On each date, only the prediction value from the latest released announcement is used — essentially estimating the previous quarter’s date using next quarter’s data. In the “Guess Tomorrow’s Weather” contest, it was as if guessing what yesterday’s weather was like in this morning
# gdp_forecasts= gdp_forecasts.sort_values('vintage_date').groupby('date', as_index=False).last()
#corrected version
gdp_forecasts= gdp_forecasts.sort_values(['vintage_date', 'forecast_horizon'])
#print(gdp_forecasts.head(15))
gdp_actual = gdp_actual.sort_values('vintage_date').groupby('date', as_index=False).last()
gdp_actual = gdp_actual.sort_values('date') #groupby 를 거치면 날짜 순서가 흐트러질 수 있음
#print(gdp_actual.head(15))

#(wrong) cpi_forecasts= cpi_forecasts.sort_values('vintage_date').groupby('date', as_index=False).last()
#corrected version
cpi_forecasts= cpi_forecasts.sort_values(['vintage_date', 'forecast_horizon'])
#print(cpi_forecasts.head(15))
cpi_actual= cpi_actual.sort_values('vintage_date').groupby('date', as_index=False).last()
cpi_actual = cpi_actual.sort_values('date') #groupby 를 거치면 날짜 순서가 흐트러질 수 있음
#print(cpi_actual.head(15))

gdp_forecasts['growth_forecast']= gdp_forecasts.groupby('vintage_date')['value'].pct_change()*100
H=4 # 몇 분기 앞 예측을 볼지 (4Q= 1년 앞), which quarter to look at(4Q= 1year ahead)
gdp_forecasts = gdp_forecasts[gdp_forecasts['forecast_horizon']==H] #df[df['column'] == value] column 이 값과 같은 행만 가져와라
gdp_actual['growth_actual']= gdp_actual['value'].pct_change()*100

cpi_forecasts['growth_forecast']= cpi_forecasts.groupby('vintage_date')['value'].pct_change()*100
cpi_forecasts = cpi_forecasts[cpi_forecasts['forecast_horizon']==H]
cpi_actual['growth_actual']= cpi_actual['value'].pct_change()*100

gdp_growth = pd.merge(gdp_forecasts[['date','growth_forecast']], gdp_actual[['date','growth_actual']], on='date', how='inner')
cpi_growth = pd.merge(cpi_forecasts[['date','growth_forecast']],cpi_actual[['date','growth_actual']],on='date', how='inner')

#print(gdp_growth.head(10))
#print(cpi_growth.head(10))

gdp_growth['error'] = gdp_growth['growth_forecast']-gdp_growth['growth_actual']
cpi_growth['error'] = cpi_growth['growth_forecast']-cpi_growth['growth_actual']

#print(gdp_growth.head())
#print(cpi_growth.head())

gdp_errors = gdp_growth['error']
cpi_errors = cpi_growth['error']

gdp_mean_error = gdp_errors.mean()
gdp_MAE = gdp_errors.abs().mean()
gdp_RMSE = np.sqrt((gdp_errors**2).mean())

cpi_mean_error = cpi_errors.mean()
cpi_MAE = cpi_errors.abs().mean()
cpi_RMSE = np.sqrt((cpi_errors**2).mean())

print("=== GDP Growth Forecast Accuracy ===")
print("Mean Error (Bias):", gdp_mean_error)
print("MAE:", gdp_MAE)
print("RMSE:", gdp_RMSE)

print("\n=== CPI Inflation Forecast Accuracy ===")
print("Mean Error (Bias):", cpi_mean_error)
print("MAE:", cpi_MAE)
print("RMSE:", cpi_RMSE)

#=== GDP Growth Forecast Accuracy (horizon=4, N=85) ===
#Mean Error (Bias): 0.2050159178605852
#MAE: 0.9283227607921085
#RMSE: 2.962173050885164
#GDP growth rate: Predicted on average 0.21 pp higher (overestimated) than actual, with MAE of 0.93 pp and RMSE of 2.96 pp (occasionally much larger than MAE due to occasional large errors — likely influenced by the COVID period)

#=== CPI Inflation Forecast Accuracy (horizon=4, N=73) ===
#Mean Error (Bias): -0.24224598259758412
#MAE: 0.5005750265922325
#RMSE: 0.7208449614986379
#CPI inflation: Predicted on average 0.24 pp lower (underestimated) than actual, MAE 0.50 pp, RMSE 0.72pp
