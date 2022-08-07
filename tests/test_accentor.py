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

import os
import sys
import unittest
from pprint import pprint


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ukrainian_accentor_transformer import Accentor


class TestAccentor(unittest.TestCase):

    @classmethod
    def setUpClass(TestAccentor):
        TestAccentor.accentor = Accentor()

    def test_simple_accent(self):
        text = "Привіт хлопче, як справи."
        accented = self.accentor(text)
        self.assertEqual(text, accented.replace("\u0301",""))

    def test_batch_accent(self):
        text1 = "Привіт хлопче, як справи."
        text2 = "в мене все добре, дякую."
        accented1, accented2 = self.accentor([text1, text2])
        self.assertEqual(text1, accented1.replace("\u0301",""))
        self.assertEqual(text2, accented2.replace("\u0301",""))

    def test_long_sentence(self):
        text = "Адже як би не оцінював галичан один страшно інтелігентний виходець з радянсько єврейських середовищ київського Подолу самі галичани вважають свою культуру і традицію політичну і релігійну побутову й господарську на голову вищою від усього що за Збручем"
        accented = self.accentor(text)
        self.assertEqual(text, accented.replace("\u0301",""))

if __name__ == '__main__':
    unittest.main()
