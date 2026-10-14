"""
Corporate Card Portfolio & Unit Economics Simulator
Author: Luis Ángeles González (Technical Product Lead)
Description: Computes gross margin, reward liabilities, and net contribution per active B2B cardholder cohort.
"""

import pandas as pd
import numpy as np

def simulate_card_portfolio_economics(df_transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Simulates monthly unit economics for a premium corporate card portfolio (Black Card tier).
    """
    INTERCHANGE_DOMESTIC_RATE = 0.015  # 1.5% effective interchange
    INTERCHANGE_CB_RATE = 0.022        # 2.2% for cross-border transactions
    REWARD_LIABILITY_RATE = 0.008      # 0.8% reward redemption cost (travel/concierge)
    OPERATING_COST_PER_USER = 120.0    # MXN monthly cost per active card

    results = df_transactions.copy()
    
    # Volume breakdown
    results['domestic_volume'] = results['total_volume_mxn'] * (1 - results['cross_border_share'])
    results['cb_volume'] = results['total_volume_mxn'] * results['cross_border_share']
    
    # Revenue & Cost computation
    results['gross_revenue'] = (
        (results['domestic_volume'] * INTERCHANGE_DOMESTIC_RATE) + 
        (results['cb_volume'] * INTERCHANGE_CB_RATE)
    )
    results['reward_costs'] = results['total_volume_mxn'] * REWARD_LIABILITY_RATE
    results['opex'] = results['active_users'] * OPERATING_COST_PER_USER
    
    # Net Margins
    results['net_contribution_margin'] = results['gross_revenue'] - results['reward_costs'] - results['opex']
    results['margin_percentage'] = (results['net_contribution_margin'] / results['gross_revenue']) * 100

    return results

if __name__ == "__main__":
    # Sample B2B cohort data
    data = {
        'cohort_month': ['2026-01', '2026-02', '2026-03'],
        'active_users': [1200, 1450, 1800],
        'total_volume_mxn': [45000000.0, 58000000.0, 75000000.0],
        'cross_border_share': [0.35, 0.40, 0.42]
    }
    
    df_input = pd.DataFrame(data)
    df_output = simulate_card_portfolio_economics(df_input)
    
    print("--- CORPORATE CARD UNIT ECONOMICS SIMULATION ---")
    print(df_output[['cohort_month', 'active_users', 'gross_revenue', 'net_contribution_margin', 'margin_percentage']])
