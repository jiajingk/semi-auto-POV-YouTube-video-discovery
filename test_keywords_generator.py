


def test_keywords_type():
    from keywords_generator import KeywordsGenerator
    keywords_gen = KeywordsGenerator()
    for keywords in keywords_gen.next_keyworks():
        assert isinstance(keywords, list)
        for keyword in keywords:
            assert isinstance(keyword, str)
            assert ' ' not in keyword
            

if __name__ == "__main__":
    test_keywords_type()