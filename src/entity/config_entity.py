from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    dir: Path
    url: Path
    local_folder:Path
    unzip_folder:Path

@dataclass
class BaseModelConfig:
    dir: Path
    base_model: Path
    update_base_model_path: Path
    image_size: list
    learning_rate: float
    include_top: bool
    weights: str
    classes :int 

@dataclass
class ModelTrainConfig:
    dir:Path
    model_path: Path
    update_base_model_path:Path
    train_data:Path
    validation_data:Path
    epochs: int
    batch_size: int
    image_size: bool
    augmentation:list        