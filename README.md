# AI Project : FAMA French Analysis
The PDF analyzes the Fama-French factor models—tools that explain stock/ETF returns beyond simple market ups/downs—using three ETFs: VTI (total U.S. market), QQQ (tech-heavy Nasdaq 100), and IWN (small-cap value stocks). It interprets regression results to show how much each ETF's performance comes from "factors" like size (small vs. big stocks), value (cheap vs. pricey), profitability, investment style, and momentum. 
**VTI (Market ETF)**: Near-perfect market tracker. Alpha (extra return from skill) is zero—expected for passive funds. R² ~99%, betas for non-market factors ~0 (factor-neutral). It's the baseline: diversified, no tilts. 

**QQQ (Growth Tech)**: Higher market beta (1.1, riskier). Negative size/value (big/glamour stocks), positive profitability/momentum. Positive alpha in simpler models shrinks in full 5-factor—outperformance explained by growth tilts, not magic. 

**IWN (Small Value)**: Positive size/value betas (harvests small/cheap premiums). Negative profitability (riskier firms). Zero alpha—returns fully from factor risks, no manager edge. 

Key insight: Market (VTI) nets factors to zero; specialized ETFs like QQQ/IWN tilt for premiums (or risks). To beat models, tilt toward rewarded factors (e.g., profitability + momentum). Bonus simulation: Factor-mimicking portfolio yields insignificant alpha, proving models work.
