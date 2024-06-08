from moviepy.editor import *
import json

def create_api(api):
    with open("api.json", 'w')as arch:
        json.dump(api,arch,indent=4)