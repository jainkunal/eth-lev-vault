from sklearn.discriminant_analysis import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from xgboost import XGBClassifier
from model.data import CORRELATION_PERIODS, INDICES, get_data
import pandas as pd
from giza.zkcook import serialize_model


def train():
    df = get_data()
    # Create target variable (1 if next day's close price is higher, else 0)
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    # Features including the new ones
    features = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "MACD",
        "Signal_Line",
        "RSI",
        "BB_Middle",
        "BB_Upper",
        "BB_Lower",
        "Stochastic",
        "ATR",
        "OBV",
        "MACD_Hist",
        "VWAP",
        "RSI_7",
        "RSI_21",
        "Momentum",
        "ROC",
        "CCI",
        "Williams_%R",
        "CMF",
        "MFI",
        "Force_Index",
        "Tenkan_Sen",
        "Kijun_Sen",
        "Senkou_Span_A",
        "Senkou_Span_B",
        "Chikou_Span",
        "RVI",
        "Keltner_Upper",
        "Keltner_Lower",
        "Donchian_Upper",
        "Donchian_Lower",
        "Vortex_Positive",
        "Vortex_Negative",
    ] + [
        f"Corr_{name}_{period}"
        for name in INDICES.keys()
        for period in CORRELATION_PERIODS
    ]

    X = df[features]
    y = df["Target"]

    # Drop the last row as it will have NaN target value
    X = X[:-1]
    y = y[:-1]

    # Polynomial Features
    poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    poly_features = poly.fit_transform(X)
    poly_feature_names = poly.get_feature_names_out(X.columns)

    # Create a DataFrame with the new features
    poly_df = pd.DataFrame(poly_features, columns=poly_feature_names, index=X.index)

    # Combine with the original features
    X_poly = pd.concat([X, poly_df], axis=1)

    # Recursive Feature Elimination
    # rf = RandomForestClassifier(n_estimators=100, random_state=42)
    # rfe = RFE(estimator=rf, n_features_to_select=20)
    # X_rfe = rfe.fit_transform(X_poly, y)
    # selected_features = X_poly.columns[rfe.support_]

    selected_features = [
        "OBV VWAP",
        "VWAP Keltner_Lower",
        "RSI_7 Vortex_Negative",
        "Williams_%R RVI",
        "Williams_%R Corr_DJIA_21",
        "CMF Corr_Gold_14",
        "Vortex_Positive Vortex_Negative",
        "Corr_DJIA_7 Corr_Gold_7",
        "Corr_DJIA_7 Corr_Gold_14",
        "Corr_DJIA_21 Corr_DJIA_28",
    ]

    X_selected = X_poly[selected_features]

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Hyperparameter tuning with GridSearchCV
    # param_grid = {
    #     'n_estimators': [100, 200, 300],
    #     'max_features': ['sqrt', 'log2', None],
    #     'max_depth': [4, 6, 8, 10, None],
    #     'min_samples_split': [2, 5, 10],
    #     'min_samples_leaf': [1, 2, 4]
    # }
    # grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
    # grid_search.fit(X_train, y_train)
    # best_params = grid_search.best_params_
    best_params = {}

    # Train with best parameters
    xg_best = XGBClassifier(**best_params, random_state=42)
    xg_best.fit(X_train, y_train)

    # Predict and evaluate the model
    y_pred = xg_best.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    return xg_best


model = train()
serialize_model(model, "xgb_eth_up_down.json")
