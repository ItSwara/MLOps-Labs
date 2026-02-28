import pandas as pd
import numpy as np
import joblib
from sklearn.inspection import permutation_importance

# Load model, scaler, label encoder
model = joblib.load('model/model.pkl')
scaler = joblib.load('model/scaler.pkl')
le = joblib.load('model/label_encoder.pkl')

FEATURES = ['MP_pg', 'PTS_pg', 'AST_pg', 'TRB_pg', 'BLK_pg', 'STL_pg',
            '3P_pg', 'FG%', 'ORB_pg', 'DRB_pg', 'TOV_pg', 'PF_pg', 'FT_pg',
            'AST%', 'TRB%', 'BLK%', 'STL%', 'USG%']

POS_MAP = {
    'PG': 'Guard', 'SG': 'Guard', 'G': 'Guard',
    'SF': 'Forward', 'PF': 'Forward', 'F': 'Forward',
    'C': 'Center'
}

# ── 1. Load & prep data ──────────────────────────────────────────────
df = pd.read_csv('src/data/nba_seasons.csv', encoding='utf-8')
df = df.drop(columns=[col for col in df.columns if 'blank' in col.lower()])
df['Pos'] = df['Pos'].str.split('-').str[0].map(POS_MAP)
df = df.dropna(subset=['Pos'])
df = df[df['Year'] >= 1980]

tot_players = df[df['Tm'] == 'TOT']['Player'].unique()
df = df[~((df['Player'].isin(tot_players)) & (df['Tm'] != 'TOT'))]
df = df[df['G'] > 0].copy()

df['MP_pg']  = df['MP']  / df['G']
df['PTS_pg'] = df['PTS'] / df['G']
df['AST_pg'] = df['AST'] / df['G']
df['TRB_pg'] = df['TRB'] / df['G']
df['BLK_pg'] = df['BLK'] / df['G']
df['STL_pg'] = df['STL'] / df['G']
df['3P_pg']  = df['3P']  / df['G']
df['ORB_pg'] = df['ORB'] / df['G']
df['DRB_pg'] = df['DRB'] / df['G']
df['TOV_pg'] = df['TOV'] / df['G']
df['PF_pg']  = df['PF']  / df['G']
df['FT_pg']  = df['FT']  / df['G']
df[FEATURES] = df[FEATURES].fillna(0)
df = df[df['MP_pg'] >= 10].dropna(subset=FEATURES)

X = df[FEATURES]
y = le.transform(df['Pos'])

# ── 2. XGBoost built-in feature importance ───────────────────────────
print("=" * 55)
print("1. XGBOOST BUILT-IN FEATURE IMPORTANCE (gain)")
print("=" * 55)
imp = model.get_booster().get_score(importance_type='gain')
imp_df = pd.DataFrame({'Feature': list(imp.keys()), 'Importance': list(imp.values())})
imp_df = imp_df.sort_values('Importance', ascending=False).reset_index(drop=True)
imp_df['Importance'] = imp_df['Importance'].round(2)
print(imp_df.to_string(index=False))

# ── 3. Permutation importance ────────────────────────────────────────
print("\n" + "=" * 55)
print("2. PERMUTATION IMPORTANCE (most reliable)")
print("=" * 55)
X_scaled = scaler.transform(X)
perm = permutation_importance(model, X_scaled, y, n_repeats=10, random_state=42, n_jobs=-1)
perm_df = pd.DataFrame({
    'Feature': FEATURES,
    'Importance': perm.importances_mean.round(4)
}).sort_values('Importance', ascending=False).reset_index(drop=True)
print(perm_df.to_string(index=False))

# ── 4. Per-position mean stats ───────────────────────────────────────
print("\n" + "=" * 55)
print("3. MEAN STATS PER POSITION (top 8 features)")
print("=" * 55)
top8 = perm_df['Feature'].head(8).tolist()
# Map advanced % features back to per-game equivalents for display
display_map = {'TRB%': 'TRB_pg', 'BLK%': 'BLK_pg', 'AST%': 'AST_pg', 
               'STL%': 'STL_pg', 'USG%': 'PTS_pg'}
display_cols = [display_map.get(f, f) for f in top8]
display_cols = [c for c in display_cols if c in df.columns]
means = df.groupby('Pos')[display_cols].mean().round(2)
print(means)

# ── 5. Sensitivity test — flip one feature at a time ────────────────
print("\n" + "=" * 55)
print("4. SENSITIVITY TEST — which features change prediction?")
print("=" * 55)

# Baseline: average Guard stats
baseline = dict(zip(FEATURES, X_scaled.mean(axis=0)))
base_input = np.array([list(baseline.values())])
base_pred = le.inverse_transform(model.predict(base_input))[0]
print(f"\nBaseline prediction: {base_pred}")
print(f"{'Feature':<15} {'Change':<20} {'New Prediction':<15} {'Changed?'}")
print("-" * 60)

for i, feat in enumerate(FEATURES):
    test = base_input.copy()
    test[0][i] += 2.0  # increase feature by 2 std devs
    new_pred = le.inverse_transform(model.predict(test))[0]
    changed = "✅ YES" if new_pred != base_pred else "❌ no"
    print(f"{feat:<15} {'+2 std devs':<20} {new_pred:<15} {changed}")