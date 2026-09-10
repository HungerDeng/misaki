from .transcription import pinyin_to_ipa
from pypinyin import lazy_pinyin, Style
from .token import MToken
from typing import List, Optional, Tuple
import cn2an
import jieba
import re

class ZHG2P:
    # unk indicates the fallback phoneme marker for unknown or unsupported text. Its default value is ❓.
    # For example, when an English segment, e.g. "OpenAI", is encountered without an en_callable, the code uses: phonemes = self.unk
    # So "OpenAI" becomes an MToken whose phonemes are ❓, indicating that the frontend could not produce a pronunciation.
    def __init__(self, version=None, unk='❓', en_callable=None):
        self.version = version
        self.frontend = None
        self.en_callable = en_callable
        self.unk = unk
        if version == '1.1':
            from .zh_frontend import ZHFrontend
            self.frontend = ZHFrontend(unk=unk)
            if en_callable is None:
                print('Warning: en_callable is None, so English may be removed')

    @staticmethod
    def retone(p):
        p = p.replace('˧˩˧', '↓') # third tone
        p = p.replace('˧˥', '↗')  # second tone
        p = p.replace('˥˩', '↘')  # fourth tone
        p = p.replace('˥', '→')   # first tone
        p = p.replace(chr(635)+chr(809), 'ɨ').replace(chr(633)+chr(809), 'ɨ')
        assert chr(809) not in p, p
        return p

    @staticmethod
    def py2ipa(py):
        return ''.join(ZHG2P.retone(p) for p in pinyin_to_ipa(py)[0])

    @staticmethod
    def word2ipa(w):
        pinyins = lazy_pinyin(w, style=Style.TONE3, neutral_tone_with_five=True)
        return ''.join(ZHG2P.py2ipa(py) for py in pinyins)

    @staticmethod
    def map_punctuation(text):
        text = text.replace('、', ', ').replace('，', ', ')
        text = text.replace('。', '. ').replace('．', '. ')
        text = text.replace('！', '! ')
        text = text.replace('：', ': ')
        text = text.replace('；', '; ')
        text = text.replace('？', '? ')
        text = text.replace('«', ' “').replace('»', '” ')
        text = text.replace('《', ' “').replace('》', '” ')
        text = text.replace('「', ' “').replace('」', '” ')
        text = text.replace('【', ' “').replace('】', '” ')
        text = text.replace('（', ' (').replace('）', ') ')
        return text.strip()

    @staticmethod
    def legacy_call(text: str) -> Tuple[str, List[MToken]]:
        """Return the base-model IPA output together with alignable text tokens."""
        tokens: List[MToken] = []
        for segment in re.findall(r'[\u4E00-\u9FFF]+|[^\u4E00-\u9FFF]+', text):
            if re.fullmatch(r'[\u4E00-\u9FFF]+', segment):
                words = jieba.lcut(segment, cut_all=False)
                for index, word in enumerate(words):
                    tokens.append(MToken(
                        text=word,
                        tag='zh',
                        whitespace=' ' if index < len(words) - 1 else '',
                        phonemes=ZHG2P.word2ipa(word).replace(chr(815), ''),
                    ))
                continue

            # Legacy ZHG2P passes punctuation and non-Mandarin text through
            # unchanged. Attach a whitespace run to the preceding token so
            # Kokoro's timestamp alignment consumes the exact same phonemes.
            for part in re.findall(r'\s+|\S+', segment):
                if part.isspace() and tokens:
                    tokens[-1].whitespace += part
                else:
                    tokens.append(MToken(text=part, tag='other', whitespace='', phonemes=part))

        return ''.join(token.phonemes + token.whitespace for token in tokens), tokens

    def __call__(self, text, en_callable=None) -> Tuple[str, Optional[List[MToken]]]:
        if not text.strip():
            return '', None
        text = cn2an.transform(text, 'an2cn')
        text = ZHG2P.map_punctuation(text)
        if self.frontend is None:
            return ZHG2P.legacy_call(text)
        # TODO: Interleaved English is brittle, needs improvement.
        en_callable = self.en_callable if en_callable is None else en_callable
        segments: List[str] = []
        tokens: List[MToken] = []
        for en, zh in re.findall(r'([A-Za-z \'-]*[A-Za-z][A-Za-z \'-]*)|([^A-Za-z]+)', text):
            en, zh = en.strip(), zh.strip()
            if zh:
                phonemes, segment_tokens = self.frontend(zh)
            else:
                phonemes = self.unk if en_callable is None else en_callable(en)
                segment_tokens = [
                    MToken(text=en, tag='eng', whitespace='', phonemes=phonemes)
                ]

            segments.append(phonemes)
            if tokens and segment_tokens:
                tokens[-1].whitespace += ' '
            tokens.extend(segment_tokens)

        return ' '.join(segments), tokens
