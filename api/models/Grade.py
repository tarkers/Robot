import cv2
import math
import mediapipe as mp
import operator

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# -2:initial ,-1:wait for answer, >0: final_answer
final_answer = -2
# detect first ,seek:not to do the work now
seek = False


class SimpleGestureDetector:
    # region: Member variables
    # mediaPipe configuration hands object
    __mpHands = mp.solutions.hands
    # mediaPipe detector objet
    __mpHandDetector = None

    def __init__(self):
        self.__setDefaultHandConfiguration()
        self.count = 0
        self.cal = [0, 0, 0, 0, 0, 0]
        self.secal = [0, 0, 0, 0, 0, 0]
        self.br = False
        self.anwser = None

    def __setDefaultHandConfiguration(self):
        self.__mpHandDetector = self.__mpHands.Hands(
            max_num_hands=2,
            # Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the hand landmarks to be considered tracked successfully (default= 0.5)
            min_detection_confidence=0.5,
            # Minimum confidence value ([0.0, 1.0]) from the hand detection model for the detection to be considered successful. (default = 0.5)
            min_tracking_confidence=0.5
        )

    def __getEuclideanDistance(self, posA, posB):
        return math.sqrt((posA.x - posB.x)**2 + (posA.y - posB.y)**2)

    def __isThumbNearIndexFinger(self, thumbPos, indexPos):
        return self.__getEuclideanDistance(thumbPos, indexPos) < 0.1

    def detectHands(self, capture):
        if self.__mpHandDetector is None:
            return None
        answer = None
        image = capture
        # image = capture.color
        # Input image must contain three channel rgb data.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # lock image for hand detection
        image.flags.writeable = False
        # start handDetector on current image
        detectorResults = self.__mpHandDetector.process(image)
        # unlock image
        image.flags.writeable = True

        if detectorResults.multi_hand_landmarks:
            for handLandmarks in detectorResults.multi_hand_landmarks:
                answer = self.simpleGesture(handLandmarks.landmark)
        return answer

    def simpleGesture(self, handLandmarks):
        thumbIsOpen = False
        indexIsOpen = False
        middelIsOpen = False
        ringIsOpen = False
        pinkyIsOpen = False

        pseudoFixKeyPoint = handLandmarks[2].x
        if handLandmarks[3].x < pseudoFixKeyPoint and handLandmarks[4].x < pseudoFixKeyPoint:
            thumbIsOpen = True

        pseudoFixKeyPoint = handLandmarks[6].y
        if handLandmarks[7].y < pseudoFixKeyPoint and handLandmarks[8].y < pseudoFixKeyPoint:
            indexIsOpen = True

        pseudoFixKeyPoint = handLandmarks[10].y
        if handLandmarks[11].y < pseudoFixKeyPoint and handLandmarks[12].y < pseudoFixKeyPoint:
            middelIsOpen = True

        pseudoFixKeyPoint = handLandmarks[14].y
        if handLandmarks[15].y < pseudoFixKeyPoint and handLandmarks[16].y < pseudoFixKeyPoint:
            ringIsOpen = True

        pseudoFixKeyPoint = handLandmarks[18].y
        if handLandmarks[19].y < pseudoFixKeyPoint and handLandmarks[20].y < pseudoFixKeyPoint:
            pinkyIsOpen = True
        if self.count == 10:
            self.count = 0
            index, value = max(enumerate(self.cal), key=operator.itemgetter(1))
            self.cal = [0, 0, 0, 0, 0, 0]
            # if value > 9:
            #   self.anwser = None
            #   return index
            if self.anwser == None or self.anwser != index:
                self.anwser = index
                return None
            else:
                self.anwser = None
                return index
        if thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen:
            # print("FIVE!")
            self.cal[5] += 1
        elif not thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen:
            # print("FOUR!")
            self.cal[4] += 1
        elif not thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and not pinkyIsOpen:
            # print("THREE!")
            self.cal[3] += 1
        elif not thumbIsOpen and indexIsOpen and middelIsOpen and not ringIsOpen and not pinkyIsOpen:
            # print("TWO!")
            self.cal[2] += 1
        elif not thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and not pinkyIsOpen:
            # print("ONE!")
            self.cal[1] += 1
        elif not thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and pinkyIsOpen:
            # print("ROCK!")
            self.cal[4] += 1
        elif thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and pinkyIsOpen:
            # print("SPIDERMAN!")
            self.cal[4] += 1
        elif not thumbIsOpen and not indexIsOpen and not middelIsOpen and not ringIsOpen and not pinkyIsOpen:
            # print("FIST!")
            self.cal[0] += 1
        elif not indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen and self.__isThumbNearIndexFinger(handLandmarks[4], handLandmarks[8]):
            pass
        self.count += 1
        return None


def retrieve_score():
    global final_answer
    s = SimpleGestureDetector()
    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success or not seek:
                # not seek means doesnt need the image now
                # print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            answer = s.detectHands(image)
            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            #resize the image 
            image = cv2.resize(image, (800, 600), interpolation=cv2.INTER_AREA)
            ret, buffer = cv2.imencode('.jpg', image)
            #prevent the null frame
            if not ret:
                continue
            # get the final answer
            if answer != None:
              final_answer = answer
              answer = None
              print("final:", final_answer)
            else:
              yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buffer) + b'\r\n')


def get_answer():
    global final_answer, seek
    if final_answer >= 0:
        answer = final_answer
        final_answer = -2
        seek=False
        return answer
    else:
        if final_answer == -2:
            seek = True
        final_answer = -1
        return -1    
  
  


# retrieve_score()
