**UK Economic Forecast Accuracy & Bias Analysis**

Research Question; How accurately do UK economic forecasts predict subsequent economic outcomes?

- This project evaluates the accuracy and systematic bias of four-quarter-ahead UK economic forecasts by comparing forecasted outcomes with subsequently realised data.

The analysis focuses on:
- UK GDP growth
- UK CPI inflation

Methodology

- Historical four-quarter-ahead forecasts are compared with realised economic outcomes.

*Forecast error is defined as: Forecast Error = Forecast − Actual

To evaluate forecast performance:

- Mean Error (Bias): measures systematic over- or under-prediction
- Mean Absolute Error (MAE): measures the average magnitude of forecast errors
- Root Mean Squared Error (RMSE): gives greater weight to large forecast errors

*A positive Mean Error indicates overprediction, while a negative Mean Error indicates underprediction.

Correcting for look-ahead bias
- An earlier version of the pipeline grouped forecasts by target date and kept only the last (most recent) vintage for each date. This inadvertently used later, more-informed vintages to stand in for earlier ones —  using information that wasn't yet available at that time. The pipeline was corrected to align each forecast strictly by its own vintage date and horizon, so that only information available at the time of the forecast is used.

Key Results

- GDP growth forecasts exhibited a positive average bias of +0.21 pp, indicating that forecasts tended to overestimate actual growth. The MAE of 0.93pp indicates the average absolute forecast error, while the substantially higher RMSE of 2.96pp suggests the presence of several unusually large forecast errors.
- CPI inflation forecasts exhibited a negative average bias of −0.24 pp, indicating that inflation was underestimated on average. Forecast accuracy was higher than for GDP growth, with an MAE of 0.50pp and an RMSE of 0.72pp.

Interpretation
- GDP growth forecasts show both a positive bias and greater sensitivity to large forecast errors, while CPI inflation forecasts display a smaller average error and lower dispersion of forecast errors.
- The difference between GDP MAE and RMSE suggests that large forecast errors have a substantial impact on GDP forecast performance, potentially reflecting periods of significant economic disruption such as the COVID-19 pandemic.
