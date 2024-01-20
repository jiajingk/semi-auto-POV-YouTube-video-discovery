
def test_correct_parse_to_dataclass():
    from test_examples import test_youtube_search_responses
    from video_search_engine import parse_youtube_response
    for response in test_youtube_search_responses:
        parsed_response = parse_youtube_response(response)
        assert parsed_response.snippet.channelId is not None
        assert parsed_response.id.videoId is not None

if __name__ == "__main__":
    test_correct_parse_to_dataclass()