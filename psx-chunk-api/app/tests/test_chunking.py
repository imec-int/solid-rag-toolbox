from app.utils.chunking import chunkOnParagraphs, chunkOnSentences, chunkOnTokens


def test_chunkOnTokens():
    assert chunkOnTokens(["a" * 1000], 100) == [
        [
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
        ]
    ]
    assert chunkOnTokens(["a" * 1000, "b" * 1000], 100) == [
        [
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
            "a" * 100,
        ],
        [
            "b" * 100,
            "b" * 100,
            "b" * 100,
            "b" * 100,
            "b" * 100,
            "b" * 100,
            "b" * 100,
            "b" * 100,
            "b" * 100,
            "b" * 100,
        ],
    ]


def test_chunkOnSentences():
    assert chunkOnSentences(["a. b. c."]) == [["a", "b", "c"]]
    assert chunkOnSentences(["a. b. c. d. e f."]) == [["a", "b", "c", "d", "e f"]]


def test_chunkOnParagraphs():
    assert chunkOnParagraphs(["a\nb\nc"]) == [["a", "b", "c"]]
    assert chunkOnParagraphs(["a\n\nbklm\ncdef"]) == [["a", "bklm", "cdef"]]
