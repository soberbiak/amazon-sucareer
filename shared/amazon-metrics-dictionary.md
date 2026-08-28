# Amazon operations metric dictionary

Use the candidate's documented business definitions when available and record any deviation from the typical formula.

| Metric | Typical formula | Required context | Common error |
| --- | --- | --- | --- |
| Sessions | Amazon-reported visits | marketplace, product scope, period | treating users and sessions as identical |
| Unit Session Percentage | ordered units / sessions | parent or child scope, period | calling it conversion without scope |
| CTR | clicks / impressions | ad type, targeting scope, period | combining formats with unlike definitions |
| CVR | orders or units / clicks or sessions | denominator, attribution window | omitting retail versus ad conversion |
| CPC | ad spend / clicks | currency, ad type, period | comparing currencies or placements directly |
| ACoS | ad spend / attributed ad sales | attribution window, campaign scope | treating it as whole-business profitability |
| TACoS | ad spend / total sales | account or product scope, period | comparing it with ACoS as if denominators match |
| ROAS | attributed ad sales / ad spend | window and currency | mixing ad return with total revenue efficiency |
| Revenue | gross or net sales | currency, tax, refund, FX treatment | omitting scope and adjustments |
| Gross margin | gross profit / revenue | cost and fee inclusion | calling contribution margin gross margin |
| Inventory age share | aged units / scoped inventory | threshold, warehouse scope, date | mixing value and unit denominators |
| In-stock rate | in-stock time or items / denominator | definition, product scope, period | hiding suppressed or stranded listings |
| Refund rate | refunded orders or units / denominator | reason set, period, lag | comparing immature cohorts |
| Forecast accuracy | method-specific | horizon, aggregation, error metric | saying accuracy without method |

Always preserve account, store, portfolio, product, listing, campaign, ad-group, keyword, or search-term scope. Pair rates with absolute values when either can mislead. Match attribution windows and cohort maturity. State whether the comparison is prior period, plan, target, control, or counterfactual estimate.
