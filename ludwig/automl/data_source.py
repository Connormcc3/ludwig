from abc import ABC, abstractmethod

from typing import List

from ludwig.automl.utils import avg_num_tokens
from ludwig.utils.image_utils import is_image_score


class DataSource(ABC):
    @property
    @abstractmethod
    def columns(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_dtype(self, column) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_distinct_values(self, column, max_values_to_return) -> (int, List[str]):
        raise NotImplementedError()

    @abstractmethod
    def get_nonnull_values(self, column) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_avg_num_tokens(self, column) -> int:
        raise NotImplementedError()

    @abstractmethod
    def is_string_type(self, dtype) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError()


class DataframeSource(DataSource):
    def __init__(self, df):
        self.df = df

    @property
    def columns(self) -> List[str]:
        return self.df.columns

    def get_dtype(self, column) -> str:
        return self.df[column].dtype.name

    def get_distinct_values(self, column, max_values_to_return) -> (int, List[str]):
        unique_values = self.df[column].unique()
        num_unique_values = len(unique_values)
        return (num_unique_values, unique_values[:max_values_to_return])

    def get_nonnull_values(self, column) -> int:
        return len(self.df[column].notnull())

    def get_image_values(self, column, sample_size=10) -> int:
        return int(sum(is_image_score(None, x) for x in self.df[column].head(sample_size)))

    def get_avg_num_tokens(self, column) -> int:
        return avg_num_tokens(self.df[column])

    def is_string_type(self, dtype) -> bool:
        return dtype in ['str', 'string', 'object']

    def __len__(self) -> int:
        return len(self.df)
