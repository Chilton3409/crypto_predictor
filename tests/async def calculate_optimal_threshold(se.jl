async def calculate_optimal_threshold(self, features_array, labels_array):
    """Use scikit-learn to form an optimal threshold to check against the predictions by the machine learning model"""
    try:
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features_array, labels_array, test_size=0.2, random_state=42)

        # Fit the scaler to the training data
        self.scaler.fit(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Calculate optimal threshold
        probabilities = self.model.predict_proba(X_test_scaled)[:, 1]
        precision, recall, thresholds = precision_recall_curve(y_test, probabilities)

        # Calculate F1-score for each threshold
        f1_scores = 2 * (precision * recall) / (precision + recall)
        f1_scores = np.nan_to_num(f1_scores)  # Handle potential NaN values

        optimal_threshold = thresholds[np.argmax(f1_scores)]
        if optimal_threshold < 0 or optimal_threshold > 1:
            logging.warning(f"Optimal threshold {optimal_threshold} is outside the expected range [0, 1]")

        return optimal_threshold
    except Exception as e:
        logging.exception(f"Error calculating optimal threshold: {e}")
        return None