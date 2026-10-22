# Brief for a second model: design of experiments for a two-zeolite selectivity test (2026-10-22)

You are asked to specify the screening stage of an experimental design. Answer as a statistician would, and say plainly what you are unsure of. Your answer will be checked by a script (docs/doe-check.py) before anyone uses it; do not claim properties your matrix does not have.

## The question being tested
Two zeolites (HZSM-5 and HMCM-22) convert ethanol to hydrocarbons. A model predicts a single length scale r* serves both materials. The test statistic is a ratio R built from a selectivity measure sigma (ethene fraction among ethene plus propene, at matched time on stream and matched conversion) and one pore dimension per material. R = 1 is the prediction. The tolerance on R must come from replicate-run repeatability.

## What is proposed so far (all provisional)
- Five factors, three levels each (coded -1, 0, +1), run separately for each material: temperature; weight hourly space velocity; ethanol partial pressure; framework Si/Al (three samples per material); water co-feed.
- The centre of the first three is the literature condition for a 2014 comparison: 500 C, 0.65 g/g/h, 0.12 atm. Low and high levels are NOT set. Do not invent them; say what you need to set them.
- The full factorial is 3^5 = 243 runs plus one control (a centre repeat) = 244 per material. This is the upper bound, not the plan.

## What I need from you
1. Two or three fractional or screening designs for ONE material, at different run counts (for example near 27 and near 81), each as a design matrix.
2. For each: the defining relation or construction, the resolution, and the full alias structure for main effects and two-factor interactions. State which interactions are confounded with which.
3. Which interactions matter most for the question: Si/Al with material, temperature with space velocity (coke and site blocking), and water co-feed with temperature. Say whether each design can separate them.
4. A replicate plan: how many centre-point repeats are needed to set the tolerance on R, and how that depends on an assumed run-to-run variance. Do NOT invent a variance; state it as an assumption to be replaced by a measurement.
5. Randomisation and blocking: catalysts age through coke, so say how to block by catalyst batch and by day.
6. Stop rules for each stage: when should the screening stop and the program be reconsidered.
7. What the screening stage cannot tell us.

## Output format (required, so it can be checked)
Give each design matrix as a CSV code block with a header row of factor names (T,WHSV,PEtOH,SiAl,Water) and coded levels -1,0,1, one run per row. Put nothing else in the code block. Then give your claims in plain text: run count, number of centre runs, resolution, and which column pairs you claim are orthogonal.

## Constraints you should flag, not assume
Each run may need catalyst regeneration or a fresh bed. Coke analysis is destructive, so not every run can have a coke value. Reactor throughput is unknown. Three Si/Al samples per material must be made or bought and are not yet in hand.
