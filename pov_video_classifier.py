import os
import cv2
import vertexai
from vertexai.vision_models import ImageTextModel, Image
from dotenv import dotenv_values
import shutil
import uuid


def sample_frames(video_path: str, folder_path: str, k: int) -> int:
    assert os.path.exists(video_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = total_frames // k
    for i in range(k):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(f"{folder_path}/{i}.jpg", frame)
        else:
            cap.release()
            return i
    cap.release()
    return k

def sample_frames_per_minute(video_path: str, folder_path: str, k: int) -> int:
    assert os.path.exists(video_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration_minutes = total_frames / fps / 60
    total_samples = int(k * duration_minutes)
    if total_samples == 0:
        return 0
    if total_samples < 10:
        return sample_frames(video_path, folder_path, 10)
    if total_samples > 100:
        return sample_frames(video_path, folder_path, 100)
    interval = total_frames // total_samples
    for i in range(total_samples):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(f"{folder_path}/{i}.jpg", frame)
        else:
            break
    cap.release()
    return total_samples

def detect_first_person(path: str) -> list[str]:
    config = dotenv_values(".env") 
    PROJECT_ID = config["GCP_PROJECT_ID"]
    LOCATION = config["GCP_LOCATION"]
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config["GCP_CREDENTIAL_PATH"]
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = ImageTextModel.from_pretrained("imagetext@001")
    source_image = Image.load_from_file(location=path)
    answers = model.ask_question(
        image=source_image,
        question="Does this image display characteristics typical of a POV shot, such as a subjective camera angle or a part of the equipment being visible?",
    )
    return answers

def measure_pov_confidence_from_frames(frame_dir: str, n_sample: int) -> float:
    from tqdm import tqdm
    scores = 0.0
    for i in tqdm(range(n_sample)):
        image_path = os.path.join(frame_dir, f'{i}.jpg')
        try:
            result = detect_first_person(image_path)[0]
        except Exception as e:
            result = 'error'
        if result.lower() == 'yes':
            scores += 1.0
        elif result.lower() == 'error':
            return -1.0
    return scores / n_sample


def measure_pov_confidence_from_video(video_dir: str) -> float:
    folder_name = str(uuid.uuid4())
    os.makedirs(folder_name)
    sample_count = sample_frames_per_minute(video_dir, folder_name, 8)
    if sample_count > 0:
        conf = measure_pov_confidence_from_frames(folder_name, sample_count)
    else:
        conf = 0.0
    shutil.rmtree(folder_name)
    return conf
