# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: test_bare_embedding.py
# time: 2:29 下午

import os
import time
import tempfile
import unittest
from kashgari.processors.sequence_processor import SequenceProcessor
from kashgari.corpus import SMP2018ECDTCorpus
from kashgari.embeddings import BareEmbedding
from kashgari.tasks.classification import BiGRU_Model
from kashgari.utils import load_model


class TestBareEmbedding(unittest.TestCase):

    def test_base_cases(self):
        x, y = SMP2018ECDTCorpus.load_data()
        embedding = BareEmbedding()
        processor = SequenceProcessor()
        processor.build_vocab(x, y)
        embedding.setup_text_processor(processor)
        res = embedding.embed(x[:10])
        max_len = max([len(i) for i in x[:10]])
        assert res.shape == (10, max_len, 100)

    def test_with_model(self):
        x, y = SMP2018ECDTCorpus.load_data('test')
        model = BiGRU_Model()
        model.fit(x, y, epochs=1)

        model_path = os.path.join(tempfile.gettempdir(), str(time.time()))
        model.save(model_path)

        new_model = load_model(model_path)
        new_model.predict(x[:10])


if __name__ == "__main__":
    unittest.main()