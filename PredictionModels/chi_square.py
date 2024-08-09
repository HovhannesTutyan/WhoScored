"""Chi-square test of independence is used to determine if a significant association
exists between two categorical variables.
Age                           Ai Usage              Total
Under 30                Yes - 312 No - 178          490
30 to 50                Yes - 273 No - 183          456 
Over 50                 Yes - 224 No - 270          494
Total                         809      631          1440

H_0: Age and AI usage are independent
H_1: Age and AI usage are dependent
X_squared = SUM((observed - expected)_squared / 2))
expected = (SUM(row)/n * SUM(column) /n) *n
degrees_of_freedom = 2 for 2*2 table
significance_level = 0.05
Chi-square table of critical values for given degrees_of_freedom and significance_level is 5.99
In our example, the x_square = 32.26 > 5.99, and H_0 hypothesis is rejected, and there is significante association.
"""
import pandas as pd

def calculate_expected_values(contingency_table):
    # Calculate the grand total
    grand_total = contingency_table.sum().sum()
    
    # Calculate row and column totals
    row_totals = contingency_table.sum(axis=1)
    column_totals = contingency_table.sum(axis=0)
    
    # Create an empty DataFrame for expected values
    expected_values = pd.DataFrame(index=contingency_table.index, columns=contingency_table.columns)
    
    # Calculate expected values
    for row in contingency_table.index:
        for col in contingency_table.columns:
            expected_values.loc[row, col] = (row_totals[row] * column_totals[col]) / grand_total
    return expected_values
def calculate_chi_square(contingency_table, expected_values):
    # Calculate the Chi-square statistic
    chi_square = ((contingency_table - expected_values) ** 2 / expected_values).sum().sum()
    return chi_square

# Example data
data = {
    'Yes': [312, 273, 224],
    'No': [178, 183, 270]
}
index = ['Under 30', '30 to 50', 'Over 50']
contingency_table = pd.DataFrame(data, index=index)

# Calculate expected values
expected_values = calculate_expected_values(contingency_table)
chi_square = calculate_chi_square(contingency_table, expected_values)

print("Contingency Table:")
print(contingency_table)
print("\nExpected Values:")
print(expected_values)
print("\nChi Squared value:")
print(chi_square) # 32.26
