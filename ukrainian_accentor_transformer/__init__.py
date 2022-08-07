# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from typing import List, Union, Tuple

from huggingface_hub import snapshot_download
import sentencepiece as spm
import ctranslate2


class Accentor:
    _hf_repo = "NeonBohdan/ukrainian-accentor-transformer@v0.1"
    
    max_len = 50
    split_tokens = set([".",",","!","?"])

    _init_config = {
        "inter_threads": 2, 
        "intra_threads": 1
    }

    _run_config = {
        "repetition_penalty": 1.2,
        "max_batch_size": 8
    }

    def __init__(self, device: str = "cpu"):
        self._init_model(device = device)

    def __call__(self, sentence: Union[List[str],str],
                        symbol: str = "stress", mode: str = "reduced") -> Union[List[str],str]:
        """
        Add word stress to texts in Ukrainian
        Args:
            sentence: sentence to accent

        Returns:
            accented_sentence

        Examples:
            Simple usage.

            >>> from ukrainian_accentor_transformer import Accentor
            >>> accentor = Accentor()
            >>> accented_sentence = accentor("Привіт хлопче")
        """

        if (type(sentence) is str):
            sentences = [sentence]
        elif (type(sentence) is list):
            sentences = sentence

        accented_sentences = self._accent(sentences=sentences, symbol=symbol, mode=mode)

        if (type(sentence) is str):
            accented_sentence = accented_sentences[0]
        elif (type(sentence) is list):
            accented_sentence = accented_sentences

        return accented_sentence

    def _accent(self, sentences: List[str], symbol: str, mode: str) -> List[str]:
        """
        Internal accent function
        Args:
            sentences: list of sentences to accent

        Returns:
            accented_sentences
        """
     
        clean_sentences = self._clean_accents(sentences)

        tokenized_sentences = self.sp.encode(clean_sentences, out_type=str)
        splitted_sentences = self._split_punctuation(tokenized_sentences)
        short_sentences = self._split_long(splitted_sentences)

        translation_batch, join_list = self._to_translation_batch(short_sentences)
        results = self.model.translate_batch(translation_batch, **self._run_config)
        accented_tokens = [result.hypotheses[0] for result in results]

        join_sentences = self._join_long(accented_tokens, join_list)
        accented_sentences = self.sp.decode(join_sentences)

        return accented_sentences

    def _clean_accents(self, sentences: List[str]) -> List[str]:
        clean_sentences = [sentence.replace("\u0301","") for sentence in sentences]
        return clean_sentences

    def _split_punctuation(self, tokenized_sentences: List[List[str]]) -> List[List[List[str]]]:
        splitted_sentences = []
        for tokenized in tokenized_sentences:
            splitted = self._split_punctuation_sentence(tokenized)
            splitted_sentences.append(splitted)
        return splitted_sentences

    def _split_punctuation_sentence(self, tokenized: List[str]) -> List[List[str]]:
        splitted = []
        start_idx = 0
        for idx, token in enumerate(tokenized, start = 1):
            if token in self.split_tokens:
                splitted.append(tokenized[start_idx:idx])
                start_idx = idx
        else:
            if (start_idx < len(tokenized)):
                splitted.append(tokenized[start_idx:])
        return splitted

    def _split_long(self, splitted_sentences: List[List[List[str]]]) -> List[List[List[str]]]:
        short_sentences = []
        for tokenized in splitted_sentences:
            short = self._split_long_sentence(tokenized)
            short_sentences.append(short)
        return short_sentences

    def _split_long_sentence(self, splitted: List[List[str]]) -> List[List[str]]:
        short = []
        for sentence in splitted:
            if (len(sentence) < self.max_len):
                short.append(sentence)
            else:
                middle_idx = self._find_middle_space(sentence)
                short.append(sentence[:middle_idx])
                short.append(sentence[middle_idx:])
        return short

    @staticmethod
    def _find_middle_space(sentence: List[str]) -> int:
        middle_idx = len(sentence) // 2
        max_shift = len(sentence) // 10
        for i in range(max_shift):
            left_idx = middle_idx-i
            right_idx = middle_idx+i
            if (sentence[left_idx][0] == "▁"):
                return left_idx
            if (sentence[right_idx][0] == "▁"):
                return right_idx
        else:
            return middle_idx

    def _to_translation_batch(self, splitted_sentences: List[List[List[str]]]) -> Tuple[List[List[str]], List[int]]:
        join_list = [len(sentence) for sentence in splitted_sentences]
        translation_batch = sum(splitted_sentences, [])
        return translation_batch, join_list

    def _join_long(self, splitted_sentences: List[List[str]], join_list: List[int]) -> List[List[str]]:
        join_sentences = []
        sentence_idx = 0
        for join_len in join_list:
            sentence = sum(splitted_sentences[sentence_idx:sentence_idx + join_len], [])
            join_sentences.append(sentence)
            sentence_idx += join_len
        return join_sentences

    def _init_model(self, device: str) -> None:
        """
        Initialize a model and tokenizer
        Args:
            device: device where to run model: "cpu" or "cuda"
        """
        repo_path = self._download_huggingface(self._hf_repo)

        self.model = ctranslate2.Translator(f"{repo_path}/ctranslate2/", device=device, **self._init_config)
        self.sp = spm.SentencePieceProcessor(model_file=f"{repo_path}/tokenizer.model")

    @staticmethod
    def _download_huggingface(repo_name: str) -> str:
        """
        Download a file from Huggingface
        Args:
            repo_name: name of repository to download

        Returns:
            repo_path
        """

        # get revision
        repo_name, *suffix = repo_name.split("@")
        revision = dict(enumerate(suffix)).get(0, None)

        repo_path = snapshot_download(repo_name, revision=revision)

        return repo_path