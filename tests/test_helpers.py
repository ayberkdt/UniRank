import pytest
import pandas as pd
import numpy as np
from unirank.utils.helpers import normalize01, normalize_inverse, normalize_keywords

def test_normalize01():
    # Value in the middle
    assert normalize01(50, 0, 100) == 0.5
    # Value at min
    assert normalize01(0, 0, 100) == 0.0
    # Value at max
    assert normalize01(100, 0, 100) == 1.0
    # Value out of bounds (should clamp)
    assert normalize01(150, 0, 100) == 1.0
    assert normalize01(-10, 0, 100) == 0.0

def test_normalize_inverse():
    assert normalize_inverse(50, 0, 100) == 0.5
    assert normalize_inverse(0, 0, 100) == 1.0
    assert normalize_inverse(100, 0, 100) == 0.0

def test_normalize_keywords():
    keywords = ["apple", "BANANA", "apple", "a"]
    normalized = normalize_keywords(keywords, min_len=2)
    # 'a' should be dropped because min_len=2
    # 'apple' should be deduplicated
    # 'BANANA' should be casefolded to 'banana'
    assert set(normalized) == {"apple", "banana"}
    assert len(normalized) == 2
