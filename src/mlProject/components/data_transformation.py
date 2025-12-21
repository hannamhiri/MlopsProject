import os
from mlProject import logger
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from mlProject.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config : DataTransformationConfig, target: str):
        self.config = config
        self.target = target
        self.df = pd.read_csv(self.config.data_path)  # Charger le dataset complet

    def handle_missing_target(self):
        self.df.dropna(subset=[self.target], inplace=True)
        if self.df[self.target].dtype == object:
            self.df[self.target] = self.df[self.target].map({'Yes':1,'No':0})
        return self

    def fill_missing_values(self):
        mean_cols = ['MinTemp','MaxTemp','Temp9am','Humidity3pm','Pressure9am','Pressure3pm']
        median_cols = ['Rainfall','WindSpeed9am','WindSpeed3pm','Humidity9am','WindGustSpeed','Sunshine']
        cat_cols = ['WindGustDir', 'WindDir9am', 'WindDir3pm','Location']

        for col in mean_cols:
            if col in self.df.columns: 
                self.df[col] = self.df[col].fillna(self.df[col].mean())
        for col in median_cols:
            if col in self.df.columns: 
                self.df[col] = self.df[col].fillna(self.df[col].median())
        for col in cat_cols:
            if col in self.df.columns: 
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])

        if 'RainToday' in self.df.columns:
            self.df['RainToday'] = self.df['RainToday'].map({'Yes':1,'No':0}).fillna(0)
        return self


    def log_transform(self):
        skewed_cols = ['Rainfall','WindGustSpeed','Sunshine','RISK_MM']
        for col in skewed_cols:
            if col in self.df.columns: self.df[col] = np.log1p(self.df[col])
        return self

    def handle_outliers(self):
        cols = ['Rainfall','WindGustSpeed','RISK_MM']
        for col in cols:
            if col in self.df.columns:
                upper = self.df[col].quantile(0.99)
                self.df[col] = np.clip(self.df[col], None, upper)
        return self

    def fix_inconsistencies(self):
        if 'MinTemp' in self.df.columns and 'MaxTemp' in self.df.columns:
            invalid = self.df['MinTemp'] > self.df['MaxTemp']
            self.df.loc[invalid, ['MinTemp','MaxTemp']] = self.df.loc[invalid, ['MaxTemp','MinTemp']].values
        if 'RainToday' in self.df.columns:
            self.df.loc[(self.df['Rainfall']>0) & (self.df['RainToday']==0), 'RainToday'] = 1
        return self

    def drop_unnecessary_columns(self):
        drop_cols = ['RISK_MM','Evaporation','Cloud9am','Cloud3pm','Temp3pm']
        for col in drop_cols:
            if col in self.df.columns: self.df.drop(columns=[col], inplace=True)
        return self

    def encode_categorical(self):
        cat_features = ['Location','WindGustDir', 'WindDir9am', 'WindDir3pm']
        for col in cat_features:
            if col in self.df.columns: 
                self.df = pd.get_dummies(self.df, columns=[col], drop_first=True)
        return self

    def extract_weekday(self):
        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Weekday'] = self.df['Date'].dt.weekday
            self.df.drop(columns='Date', inplace=True)
        return self

    def transform_and_split(self, test_size=0.20, random_state=42):
        # Applique toutes les transformations
        self.handle_missing_target()\
            .fill_missing_values()\
            .log_transform()\
            .handle_outliers()\
            .fix_inconsistencies()\
            .drop_unnecessary_columns()\
            .encode_categorical()\
            .extract_weekday()

        # Split train/test
        train, test = train_test_split(self.df, test_size=test_size, random_state=random_state)

        # Sauvegarde
        os.makedirs(self.config.root_dir, exist_ok=True)
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

        logger.info("Data transformed and split into training and test sets")
        logger.info(f"Train shape: {train.shape}, Test shape: {test.shape}")
        print(f"Train shape: {train.shape}, Test shape: {test.shape}")
