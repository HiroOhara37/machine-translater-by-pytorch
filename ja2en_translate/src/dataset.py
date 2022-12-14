import pandas as pd
import torch
from torch import Tensor
from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self, df: pd.DataFrame, ja_tokenizer, en_tokenizer) -> None:
        # 単語の数値化 & padding
        # このコードだと大きなデータセットはメモリオーバーする
        # self.src_ids: list[list[int]] = ja_tokenizer(list(df["ja"]))[
        #    "input_ids"
        # ]
        # self.tgt_ids: list[list[int]] = en_tokenizer(list(df["en"]))[
        #    "input_ids"
        # ]
        self.src_ids: list[list[int]] = []
        for idx, src in enumerate(list(df["ja"])):
            if idx % 100000 == 0:
                print(f"read src data {idx}")
            self.src_ids.append(ja_tokenizer(src)["input_ids"])

        self.tgt_ids: list[list[int]] = []
        for idx, tgt in enumerate(list(df["en"])):
            if idx % 100000 == 0:
                print(f"read tgt data {idx}")
            self.tgt_ids.append(en_tokenizer(tgt)["input_ids"])

    def __len__(self) -> int:
        return len(self.src_ids)

    def __getitem__(self, index: int) -> tuple[Tensor, Tensor]:
        """
        return: tuple[TensorType["text_len", long], TensorType["text_len", long]]
        """
        # TensorType["text_len", long]
        src: Tensor = torch.LongTensor(self.src_ids[index])
        # TensorType["text_len", long]
        tgt: Tensor = torch.LongTensor(self.tgt_ids[index])

        return src, tgt
