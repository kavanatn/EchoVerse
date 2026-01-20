def concated_text(emotion_obj):
    op = ""
    for i in emotion_obj:
        op += i["speech_text"] + "\n"

    return op
