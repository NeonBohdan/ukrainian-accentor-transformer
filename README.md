# Ukrainian Accentor Transformer

This repository contains a model to make accents in Ukrainian words.

## Installation

```bash
pip install git+https://github.com/NeonBohdan/ukrainian-accentor-transformer.git
```

## Example

```python
>>> from ukrainian_accentor_transformer import Accentor
>>> text = "Кам'янець-Подільський - місто в Хмельницькій області України, центр Кам'янець-Подільської міської об'єднаної територіальної громади і Кам'янець-Подільського району."
>>> accentor = Accentor()
>>> accentor(text)

"Кам'яне́ць-Поді́льський - мі́сто в Хмельни́цькій о́бласті Украї́ни, центр Кам'яне́ць-Поді́льської місько́ї об'є́днаної територіа́льної грома́ди і Кам'яне́ць-Поді́льського райо́ну."
```

## Attribution

Trained on dataset - [News corpus](https://lang.org.ua/en/corpora/#anchor5) by [Dmytro Chaplynskyi](https://github.com/dchaplinsky) from [lang-uk](https://github.com/lang-uk)\
Stressed using [ukrainian-word-stress](https://github.com/lang-uk/ukrainian-word-stress) by [Oleksiy Syvokon](https://github.com/asivokon)