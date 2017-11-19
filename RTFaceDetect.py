import requests, json, cv2, time, operator

#Enter your key
subscription_key = ''
#Choose your server (default: West Europe)
url_base = 'https://westeurope.api.cognitive.microsoft.com'
#Choose number of your video input (default: 0)
video_input = 0
#Choose output (0:Short, 1:Complete (default: 0))
output = 1

while True:
    camera = cv2.VideoCapture(video_input)
    if camera.read()[1] is not None:
        break
    print("Camera not found!")
    print("Next attempt in 10 seconds.")
    time.sleep(10)
print("Camera found, starting video.")
print("Press Q to exit.")
headers = {
     'Content-type': 'application/octet-stream',
     'Ocp-Apim-Subscription-Key': subscription_key,
}
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

seconds = time.time()
while(True):
    frame = camera.read()[1]
    cv2.imshow('Camera',frame)

    if abs(time.time() - seconds) >= 10:
        body = cv2.imencode(".jpg", frame)[1].tobytes()
        try:
            response = requests.request('POST', url_base + '/face/v1.0/detect', params=params, data=body, headers=headers)
            #print ('Response:', response)
            parsed = json.loads(response.text)
            if parsed == []:
                print("No face detect")
            else:
                if output == 0:
                    face = parsed[0]["faceAttributes"]
                    print("\nGender: {}\nAge: about {}\nGlasses: {}\nHair Color: {}\nEmotion: {}".format(face["gender"], face["age"], face["glasses"], face["hair"]["hairColor"][0]["color"], max(face["emotion"].items(), key=operator.itemgetter(1))[0]))
                else:
                    print(json.dumps(parsed, sort_keys=True, indent=2))

        except:
            print('Error: Check your internet connection, subscription key, your server, and that the service is active on your account')
        seconds = time.time()
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
