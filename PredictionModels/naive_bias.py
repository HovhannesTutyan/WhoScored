from etna.analysis import plot_imputation
from etna.transforms import TimeSeriesImputerTransform

ts = get_ts(["All_American_Ensign"])
imputer = TimeSeriesImputerTransform(in_column="target", strategy="zero")
print(imputer)