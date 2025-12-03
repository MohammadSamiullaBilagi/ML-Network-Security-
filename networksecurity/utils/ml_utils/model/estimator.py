# from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

# import os
# import sys

# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging

# class NetworkModel:
#     def __init__(self,preprocessor,model):
#         try:
#             self.model=model
#             self.preprocessor=preprocessor
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)

#     def predict(self,x):
#         try:
#             x_transform=self.preprocessor.transform(x)
#             y_hat=self.model.predict(x_transform)
#             return y_hat
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)

# networksecurity/utils/ml_utils/model/estimator.py
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os
import sys
import pandas as pd
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def _to_numpy(self, X):
        """Convert common input types to numpy array expected by sklearn."""
        if isinstance(X, pd.DataFrame) or isinstance(X, pd.Series):
            return X.values
        if isinstance(X, list):
            return np.array(X)
        return X

    def predict(self, x):
        try:
            # 1) If preprocessor is present and has transform -> use it
            if self.preprocessor is not None and hasattr(self.preprocessor, "transform"):
                X_transformed = self.preprocessor.transform(x)
                return self.model.predict(X_transformed)

            # 2) If preprocessor is present but doesn't have transform (unexpected) -> try fit_transform as last resort
            if self.preprocessor is not None and hasattr(self.preprocessor, "fit_transform"):
                X_transformed = self.preprocessor.fit_transform(x)
                return self.model.predict(X_transformed)

            # 3) If preprocessor is None or not usable -> try converting input to numpy and pass to model
            X_input = self._to_numpy(x)
            return self.model.predict(X_input)

        except Exception as e:
            # Add helpful diagnostic information
            preproc_type = type(self.preprocessor).__name__ if self.preprocessor is not None else "None"
            model_type = type(self.model).__name__ if self.model is not None else "None"
            msg = (
                f"NetworkModel.predict failed. preprocessor type: {preproc_type}, "
                f"model type: {model_type}, error: {e}"
            )
            logging.error(msg)
            raise NetworkSecurityException(msg, sys) from e
