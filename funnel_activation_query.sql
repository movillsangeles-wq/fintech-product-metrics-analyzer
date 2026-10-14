-- Funnel & Activation Analysis for Corporate Card Cohorts
-- Tracks merchant/user onboarding steps and 30-day transaction activation

SELECT 
    DATE_TRUNC('month', u.created_at) AS signup_cohort,
    COUNT(DISTINCT u.user_id) AS total_signups,
    COUNT(DISTINCT CASE WHEN kyc.status = 'approved' THEN u.user_id END) AS kyc_approved,
    COUNT(DISTINCT CASE WHEN c.card_activated_at IS NOT NULL THEN u.user_id END) AS cards_activated,
    COUNT(DISTINCT CASE WHEN t.transaction_id IS NOT NULL THEN u.user_id END) AS active_transacting_users,
    ROUND(COUNT(DISTINCT CASE WHEN t.transaction_id IS NOT NULL THEN u.user_id END) * 100.0 / NULLIF(COUNT(DISTINCT u.user_id), 0), 2) AS overall_conversion_rate_pct
FROM users u
LEFT JOIN kyc_submissions kyc ON u.user_id = kyc.user_id
LEFT JOIN corporate_cards c ON u.user_id = c.user_id
LEFT JOIN transactions t ON u.user_id = t.user_id AND t.created_at >= c.card_activated_at AND t.created_at <= c.card_activated_at + INTERVAL '30 days'
WHERE u.created_at >= '2026-01-01'
GROUP BY 1
ORDER BY 1 DESC;
