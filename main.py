import os
from video_search_engine import download_youtube_video, search_youtube
from pov_video_classifier import measure_pov_confidence_from_video
from test_examples import test_youtube_urls
from keywords_generator import KeywordsGenerator
def measure_url_score(url):
    download_file_path = download_youtube_video(url)
    score = -1.0
    if download_file_path is not None:
        score = measure_pov_confidence_from_video(download_file_path)
        os.remove(download_file_path)
    
    return score
print("url, score")
key_words_gen = KeywordsGenerator()
for keywords in key_words_gen.next_keyworks(take=1):
    for url in search_youtube(keywords):
        print(f"{url}, {measure_url_score(url)}")

