import pandas as pd
from rapidfuzz import fuzz
from rapidfuzz import process

# Example datasets
claims = pd.DataFrame({
    'Policy_Number': ['P123', 'P124', 'P125'],
    'Street_Address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
    'Claim_Amount': [1000, 1500, 2000]
})

policies = pd.DataFrame({
    'Policy_Number': ['P123', 'P124', 'P126'],
    'Street_Address': ['123 Main Street', '456 Oak Avenue', '789 Pine Drive'],
    'Policy_Type': ['Home', 'Auto', 'Life']
})

# Function to perform the fuzzy matching and join
def fuzzy_join(claims, policies, threshold=80):
    # Ensure Policy_Number is the same type
    claims['Policy_Number'] = claims['Policy_Number'].astype(str)
    policies['Policy_Number'] = policies['Policy_Number'].astype(str)

    # Prepare result dataframe
    result = claims.copy()

    # Add a column to store matches
    matched_addresses = []
    matched_ratios = []
    matched_policy_data = []

    # Iterate through the claims dataset
    for _, claim_row in claims.iterrows():
        policy_matches = policies[policies['Policy_Number'] == claim_row['Policy_Number']]

        if not policy_matches.empty:
            # Perform fuzzy matching within the subset of matching policy numbers
            best_match = None
            best_ratio = 0
            best_policy_row = None

            for _, policy_row in policy_matches.iterrows():
                ratio = fuzz.ratio(claim_row['Street_Address'], policy_row['Street_Address'])
                if ratio > best_ratio:
                    best_match = policy_row['Street_Address']
                    best_ratio = ratio
                    best_policy_row = policy_row

            if best_ratio >= threshold:
                matched_addresses.append(best_match)
                matched_ratios.append(best_ratio)
                matched_policy_data.append(best_policy_row)
            else:
                matched_addresses.append(None)
                matched_ratios.append(None)
                matched_policy_data.append(pd.Series(index=policies.columns))
        else:
            matched_addresses.append(None)
            matched_ratios.append(None)
            matched_policy_data.append(pd.Series(index=policies.columns))

    # Append matched addresses, ratios, and other policy columns to the claims dataset
    result['Matched_Address'] = matched_addresses
    result['Match_Ratio'] = matched_ratios

    for col in policies.columns:
        if col != 'Policy_Number' and col != 'Street_Address':
            result[col] = [match[col] if match is not None else None for match in matched_policy_data]

    return result

# Perform the join
result = fuzzy_join(claims, policies, threshold=80)

print(result)
