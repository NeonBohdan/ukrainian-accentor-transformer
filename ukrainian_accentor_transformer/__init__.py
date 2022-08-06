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


from typing import List, Union

from huggingface_hub import snapshot_download
import sentencepiece as spm
import ctranslate2


class Accentor:
    _hf_repo = "NeonBohdan/ukrainian-accentor-transformer@v0.1"

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
     
        tokenized = self.sp.encode(sentences, out_type=str)

        results = self.model.translate_batch(tokenized, **self._run_config)

        accented_tokens = [result.hypotheses[0] for result in results]

        accented_sentences = self.sp.decode(accented_tokens)

        return accented_sentences

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