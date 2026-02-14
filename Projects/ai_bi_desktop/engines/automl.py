"""
AutoML Engine
============
Automatically selects and optimizes the best machine learning model
using Optuna for hyperparameter optimization.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import optuna
from optuna.samplers import TPESampler
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error,
    confusion_matrix, classification_report
)
from category_encoders import TargetEncoder, OrdinalEncoder

# Models
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, \
    GradientBoostingRegressor, ExtraTreesRegressor, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVR, SVC
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor

from loguru import logger
from config.settings import automl_config, evaluation_config


@dataclass
class ModelResult:
    """Results from training a single model"""
    model_name: str
    model_type: str  # 'classification' or 'regression'
    model: Any
    pipeline: Pipeline
    cv_scores: np.ndarray
    mean_cv_score: float
    std_cv_score: float
    best_params: Dict[str, Any]
    metrics: Dict[str, float]
    feature_importance: Optional[pd.DataFrame]
    reasoning: List[str]
    
    def __repr__(self):
        return f"ModelResult({self.model_name}, CV: {self.mean_cv_score:.4f}±{self.std_cv_score:.4f})"


class AutoMLEngine:
    """
    Intelligent AutoML system using Optuna for model selection and hyperparameter optimization
    """
    
    def __init__(self):
        self.config = automl_config
        self.eval_config = evaluation_config
        logger.info("AutoML Engine initialized")
        
        # Suppress Optuna logging
        optuna.logging.set_verbosity(optuna.logging.WARNING)
    
    def auto_train(self,
                   df: pd.DataFrame,
                   target_col: str,
                   task_type: str,
                   test_size: float = 0.2) -> Tuple[ModelResult, List[ModelResult]]:
        """
        Main method to automatically train and select the best model
        
        Args:
            df: Input dataframe
            target_col: Target column name
            task_type: 'regression', 'binary_classification', 'multiclass_classification'
            test_size: Test set proportion
            
        Returns:
            (best_model_result, all_model_results)
        """
        logger.info(f"Starting AutoML for {task_type} task on {target_col}")
        
        # Prepare data
        X, y, feature_names, categorical_features = self._prepare_data(df, target_col, task_type)
        
        # Get models to try based on task type
        model_configs = self._get_model_configs(task_type)
        
        logger.info(f"Training {len(model_configs)} models with Optuna optimization")
        
        all_results = []
        
        for model_name, model_factory in model_configs.items():
            try:
                logger.info(f"Optimizing {model_name}...")
                
                result = self._optimize_model(
                    X, y, model_name, model_factory, task_type,
                    feature_names, categorical_features
                )
                
                if result:
                    all_results.append(result)
                    logger.info(f"  ✓ {model_name}: {result.mean_cv_score:.4f}±{result.std_cv_score:.4f}")
                    
            except Exception as e:
                logger.error(f"Failed to train {model_name}: {e}")
        
        if not all_results:
            raise ValueError("No models were successfully trained")
        
        # Select best model
        all_results.sort(key=lambda x: x.mean_cv_score, reverse=True)
        best_model = all_results[0]
        
        logger.info(f"Best model: {best_model.model_name} (CV: {best_model.mean_cv_score:.4f})")
        
        # Add reasoning for selection
        best_model.reasoning = self._generate_model_selection_reasoning(best_model, all_results)
        
        return best_model, all_results
    
    def _prepare_data(self, 
                     df: pd.DataFrame,
                     target_col: str,
                     task_type: str) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str]]:
        """
        Prepare data for model training
        """
        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Encode target if classification
        if task_type != 'regression':
            le = LabelEncoder()
            y = pd.Series(le.fit_transform(y), index=y.index, name=target_col)
        
        # Identify categorical features
        categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        feature_names = X.columns.tolist()
        
        return X, y, feature_names, categorical_features
    
    def _get_model_configs(self, task_type: str) -> Dict[str, callable]:
        """
        Get model factories based on task type
        """
        if task_type == 'regression':
            return {
                'random_forest': lambda params: RandomForestRegressor(**params, random_state=42),
                'extra_trees': lambda params: ExtraTreesRegressor(**params, random_state=42),
                'xgboost': lambda params: XGBRegressor(**params, random_state=42, verbosity=0),
                'lightgbm': lambda params: LGBMRegressor(**params, random_state=42, verbose=-1),
                'catboost': lambda params: CatBoostRegressor(**params, random_state=42, verbose=0),
                'linear_regression': lambda params: LinearRegression(**params),
                'elasticnet': lambda params: ElasticNet(**params, random_state=42),
                'svr': lambda params: SVR(**params)
            }


        else:  # classification

            return {

                'random_forest': lambda params: RandomForestClassifier(**params, random_state=42),

                'extra_trees': lambda params: ExtraTreesClassifier(**params, random_state=42),

                'xgboost': lambda params: XGBClassifier(**params, random_state=42, verbosity=0, eval_metric='logloss'),

                'lightgbm': lambda params: LGBMClassifier(**params, random_state=42, verbose=-1),

                'catboost': lambda params: CatBoostClassifier(**params, random_state=42, verbose=0),

                'gradient_boosting': lambda params: GradientBoostingClassifier(**params, random_state=42),

                'logistic_regression': lambda params: LogisticRegression(**params, max_iter=1000, random_state=42),

                'adaboost': lambda params: AdaBoostClassifier(**params, random_state=42),

                'svc': lambda params: SVC(**params, probability=True, random_state=42)

            }

    def _optimize_model(self,
                       X: pd.DataFrame,
                       y: pd.Series,
                       model_name: str,
                       model_factory: callable,
                       task_type: str,
                       feature_names: List[str],
                       categorical_features: List[str]) -> Optional[ModelResult]:
        """
        Optimize a single model using Optuna
        """
        
        def objective(trial):
            # Suggest hyperparameters
            params = self._suggest_hyperparameters(trial, model_name, task_type)
            
            # Create model
            model = model_factory(params)
            
            # Create preprocessing pipeline
            pipeline = self._create_pipeline(model, categorical_features, X.columns.tolist())
            
            # Cross-validation
            if task_type == 'regression':
                cv = KFold(n_splits=self.config.cv_folds, shuffle=True, random_state=42)
                scoring = 'r2'
            else:
                cv = StratifiedKFold(n_splits=self.config.cv_folds, shuffle=True, random_state=42)
                scoring = 'roc_auc' if len(np.unique(y)) == 2 else 'accuracy'
            
            try:
                scores = cross_val_score(pipeline, X, y, cv=cv, scoring=scoring, n_jobs=-1)
                return scores.mean()
            except Exception as e:
                logger.debug(f"Trial failed for {model_name}: {e}")
                return -np.inf
        
        # Create Optuna study
        study = optuna.create_study(
            direction='maximize',
            sampler=TPESampler(seed=42)
        )
        
        # Optimize
        study.optimize(
            objective,
            n_trials=self.config.n_trials,
            timeout=self.config.optimization_timeout_seconds,
            show_progress_bar=False
        )
        
        if study.best_trial.value == -np.inf:
            logger.warning(f"All trials failed for {model_name}")
            return None
        
        # Train final model with best parameters
        best_params = study.best_params
        model = model_factory(best_params)
        pipeline = self._create_pipeline(model, categorical_features, X.columns.tolist())
        
        # Perform cross-validation
        if task_type == 'regression':
            cv = KFold(n_splits=self.config.cv_folds, shuffle=True, random_state=42)
            scoring = 'r2'
        else:
            cv = StratifiedKFold(n_splits=self.config.cv_folds, shuffle=True, random_state=42)
            scoring = 'roc_auc' if len(np.unique(y)) == 2 else 'accuracy'
        
        cv_scores = cross_val_score(pipeline, X, y, cv=cv, scoring=scoring, n_jobs=-1)
        
        # Fit final model on all data
        pipeline.fit(X, y)
        
        # Compute detailed metrics
        y_pred = pipeline.predict(X)
        metrics = self._compute_metrics(y, y_pred, task_type)
        
        # Extract feature importance if available
        feature_importance = self._extract_feature_importance(pipeline, feature_names)
        
        return ModelResult(
            model_name=model_name,
            model_type=task_type,
            model=model,
            pipeline=pipeline,
            cv_scores=cv_scores,
            mean_cv_score=cv_scores.mean(),
            std_cv_score=cv_scores.std(),
            best_params=best_params,
            metrics=metrics,
            feature_importance=feature_importance,
            reasoning=[]
        )
    
    def _suggest_hyperparameters(self, trial, model_name: str, task_type: str) -> Dict:
        """
        Suggest hyperparameters for Optuna trial
        """
        params = {}

        # Scale factor to reduce complexity if dataset has many features
        scale = 1

        if model_name == 'random_forest':
            params['n_estimators'] = trial.suggest_int('n_estimators', 50, 200 // scale)
            params['max_depth'] = trial.suggest_int('max_depth', 6, 15)
            params['min_samples_split'] = trial.suggest_int('min_samples_split', 2, 5)
            params['min_samples_leaf'] = trial.suggest_int('min_samples_leaf', 1, 3)

        elif model_name == 'xgboost':
            params['n_estimators'] = trial.suggest_int('n_estimators', 50, 200 // scale)
            params['max_depth'] = trial.suggest_int('max_depth', 6, 15)
            params['learning_rate'] = trial.suggest_float('learning_rate', 0.01, 0.3, log=True)
            params['subsample'] = trial.suggest_float('subsample', 0.6, 0.9)
            params['colsample_bytree'] = trial.suggest_float('colsample_bytree', 0.6, 1.0)

        elif model_name == 'catboost':
            params['iterations'] = trial.suggest_int('iterations', 50, 200 // scale)
            params['depth'] = trial.suggest_int('depth', 5, 15)
            params['learning_rate'] = trial.suggest_float('learning_rate', 0.01, 0.3, log=True)
            params['l2_leaf_reg'] = trial.suggest_float('l2_leaf_reg', 1, 10)

        elif model_name == 'linear_regression':
            # LinearRegression בדרך כלל אין הרבה פרמטרים למיקוד
            pass

        elif model_name == 'gradient_boosting':
            params['n_estimators'] = trial.suggest_int('n_estimators', 50, 200 // scale)
            params['max_depth'] = trial.suggest_int('max_depth', 4, 15)
            params['learning_rate'] = trial.suggest_float('learning_rate', 0.01, 0.3, log=True)

        return params
    
    def _create_pipeline(self, model, categorical_features: List[str], all_features: List[str]) -> Pipeline:
        """
        Create preprocessing pipeline
        """
        numeric_features = [f for f in all_features if f not in categorical_features]
        
        # Numeric transformer
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', RobustScaler())
        ])

        # בודקים סוג מודל כדי לבחור encoder חכם
        tree_models = (
            RandomForestClassifier, RandomForestRegressor,
            ExtraTreesClassifier, ExtraTreesRegressor,
            GradientBoostingClassifier, GradientBoostingRegressor,
            XGBClassifier, XGBRegressor,
            LGBMClassifier, LGBMRegressor,
            CatBoostClassifier, CatBoostRegressor,
            AdaBoostClassifier
        )

        linear_models = (
            LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet, SVR, SVC
        )

        if isinstance(model, tree_models):
            cat_encoder = TargetEncoder()
        elif isinstance(model, linear_models):
            cat_encoder = OneHotEncoder(handle_unknown='ignore')
        else:
            # ברירת מחדל – TargetEncoder
            cat_encoder = TargetEncoder()

        # Categorical transformer
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', cat_encoder)
        ])
        
        # Combine
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ],
            remainder='passthrough'
        )
        
        # Full pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        return pipeline
    
    def _compute_metrics(self, y_true, y_pred, task_type: str) -> Dict[str, float]:
        """
        Compute evaluation metrics
        """
        metrics = {}
        
        if task_type == 'regression':
            metrics['r2'] = r2_score(y_true, y_pred)
            metrics['mae'] = mean_absolute_error(y_true, y_pred)
            metrics['rmse'] = np.sqrt(mean_squared_error(y_true, y_pred))
            try:
                metrics['mape'] = mean_absolute_percentage_error(y_true, y_pred)
            except:
                metrics['mape'] = None
        else:
            metrics['accuracy'] = accuracy_score(y_true, y_pred)
            metrics['precision'] = precision_score(y_true, y_pred, average='weighted', zero_division=0)
            metrics['recall'] = recall_score(y_true, y_pred, average='weighted', zero_division=0)
            metrics['f1'] = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        return metrics
    
    def _extract_feature_importance(self, pipeline, feature_names: List[str]) -> Optional[pd.DataFrame]:
        """
        Extract feature importance from model
        """
        try:
            model = pipeline.named_steps['model']
            
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
            elif hasattr(model, 'coef_'):
                importances = np.abs(model.coef_).flatten()
            else:
                return None
            
            # Ensure correct length
            if len(importances) != len(feature_names):
                return None
            
            fi_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            return fi_df
            
        except Exception as e:
            logger.debug(f"Could not extract feature importance: {e}")
            return None
    
    def _generate_model_selection_reasoning(self,
                                           best_model: ModelResult,
                                           all_models: List[ModelResult]) -> List[str]:
        """
        Generate reasoning for why a model was selected
        """
        reasoning = []
        
        # Best performance
        reasoning.append(
            f"{best_model.model_name} achieved the highest cross-validation score: "
            f"{best_model.mean_cv_score:.4f}±{best_model.std_cv_score:.4f}"
        )
        
        # Performance gap
        if len(all_models) > 1:
            second_best = all_models[1]
            gap = best_model.mean_cv_score - second_best.mean_cv_score
            if gap > 0.05:
                reasoning.append(
                    f"Significantly outperformed {second_best.model_name} by {gap:.4f} points"
                )
            else:
                reasoning.append(
                    f"Marginally better than {second_best.model_name} ({second_best.mean_cv_score:.4f})"
                )
        
        # Model characteristics
        if 'catboost' in best_model.model_name.lower():
            reasoning.append("CatBoost handles categorical features efficiently without encoding")
        elif 'xgboost' in best_model.model_name.lower():
            reasoning.append("XGBoost provides excellent performance with built-in regularization")
        elif 'lightgbm' in best_model.model_name.lower():
            reasoning.append("LightGBM offers fast training and good performance on large datasets")
        elif 'random_forest' in best_model.model_name.lower():
            reasoning.append("Random Forest is robust and interpretable with built-in feature importance")
        elif 'extra_trees' in best_model.model_name.lower():
            reasoning.append("Extra Trees reduces overfitting by adding extra randomness to tree splits")
        elif 'gradient_boosting' in best_model.model_name.lower():
            reasoning.append("Gradient Boosting builds an ensemble of trees sequentially to reduce bias")
        elif 'linear_regression' in best_model.model_name.lower():
            reasoning.append("Linear Regression is simple, interpretable, and works well with linear relationships")
        elif 'elasticnet' in best_model.model_name.lower():
            reasoning.append("ElasticNet combines L1 and L2 regularization to handle multicollinearity")
        elif 'svr' in best_model.model_name.lower():
            reasoning.append("SVR (Support Vector Regression) is effective for small datasets with complex patterns")
        elif 'logistic_regression' in best_model.model_name.lower():
            reasoning.append("Logistic Regression is simple and interpretable, good for baseline classification")
        elif 'adaboost' in best_model.model_name.lower():
            reasoning.append("AdaBoost boosts weak learners sequentially to improve classification performance")
        elif 'svc' in best_model.model_name.lower():
            reasoning.append(
                "SVC (Support Vector Classifier) handles high-dimensional data well and allows flexible kernels")

        return reasoning

