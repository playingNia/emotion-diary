import os
import yaml

# diary.yaml 파일이 존재하지 않을 시 빈 파일 생성
if not os.path.exists("diary.yaml"):
    with open("diary.yaml", 'w') as file:
        yaml.dump({}, file)

# diary.yaml 파일 열기
with open("diary.yaml", 'r') as file:
    diary = yaml.safe_load(file)

def get_diaries():
    return diary

def get_diary(date):
    global diary
    if date not in diary:
        return ()

    data = diary[date]
    return (data["content"], data["comment"])

def set_diary(date, content, comment):
    diary[date] = {"content": content, "comment": comment}

def remove_diary(date):
    del diary[date]