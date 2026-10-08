import cv2
import time
import threading
import queue
import os

from ultralytics import YOLOWorld
from gtts import gTTS
import pygame


# ============================================================
# SETTINGS
# ============================================================

CONF_THRESH = 0.30

# Wait at least this long before another speech
SPEAK_INTERVAL = 2.5

# Repeat the current scene after this time
REFRESH_INTERVAL = 5.0


# ============================================================
# LANGUAGE SELECTION
# ============================================================

def choose_language():

    print()
    print("========================================")
    print("             SEE FOR ALL")
    print("========================================")
    print()
    print("Choose your language:")
    print()
    print("1. English")
    print("2. Hindi")
    print("3. Kannada")
    print("4. Tamil")
    print("5. Telugu")
    print()

    language_options = {
        "1": ("en", "English"),
        "2": ("hi", "Hindi"),
        "3": ("kn", "Kannada"),
        "4": ("ta", "Tamil"),
        "5": ("te", "Telugu")
    }

    while True:

        choice = input("Enter your choice (1-5): ").strip()

        if choice in language_options:

            language_code, language_name = language_options[choice]

            print()
            print("Selected language:", language_name)
            print()

            return language_code

        print(
            "Invalid choice. Please enter 1, 2, 3, 4, or 5."
        )


LANGUAGE = choose_language()


# ============================================================
# OBJECT VOCABULARY
# ============================================================

OBJECTS = [

    # People
    "person",

    # Vehicles
    "bicycle",
    "car",
    "motorcycle",
    "bus",
    "truck",
    "train",
    "airplane",
    "boat",

    # Surroundings
    "door",
    "window",
    "stairs",
    "staircase",
    "wall",
    "floor",
    "ceiling",
    "door handle",

    # Furniture
    "chair",
    "table",
    "desk",
    "sofa",
    "couch",
    "bed",
    "bench",

    # Electronics
    "laptop",
    "computer",
    "keyboard",
    "mouse",
    "mobile phone",
    "smartphone",
    "tablet",
    "television",
    "remote control",
    "camera",
    "speaker",
    "headphones",

    # Daily objects
    "bottle",
    "water bottle",
    "cup",
    "glass",
    "plate",
    "bowl",
    "spoon",
    "fork",
    "knife",

    # Stationery
    "book",
    "notebook",
    "pen",
    "pencil",
    "eraser",
    "ruler",

    # Bags / accessories
    "bag",
    "backpack",
    "handbag",
    "suitcase",
    "wallet",
    "umbrella",

    # Clothing
    "shirt",
    "pants",
    "shoe",
    "helmet",
    "hat",
    "tie",
    "glasses",
    "watch",

    # Medical
    "medicine",
    "medicine bottle",
    "pill",
    "medical box",
    "first aid box",

    # Household
    "light switch",
    "electrical socket",
    "fan",
    "refrigerator",
    "microwave",
    "oven",
    "toaster",
    "sink",

    # Traffic
    "traffic light",
    "stop sign",
    "fire hydrant",
    "parking meter",

    # Animals
    "dog",
    "cat",
    "bird",
    "horse",
    "cow",
    "sheep",
    "elephant",
    "bear",
    "zebra",
    "giraffe",

    # Plants
    "tree",
    "plant",
    "flower",
    "potted plant",

    # Food
    "food",
    "pizza",
    "cake",
    "apple",
    "banana",
    "orange",
    "sandwich",

    # Other
    "scissors",
    "teddy bear",
    "toothbrush",
    "hair dryer",
    "key",
    "money"
]


# ============================================================
# TRANSLATIONS
# ============================================================

# Format:
# English object : [Hindi, Kannada, Tamil, Telugu]

TRANSLATIONS = {

    "person": ["व्यक्ति", "ವ್ಯಕ್ತಿ", "நபர்", "వ్యక్తి"],
    "bicycle": ["साइकिल", "ಸೈಕಲ್", "மிதிவண்டி", "సైకిల్"],
    "car": ["कार", "ಕಾರು", "கார்", "కారు"],
    "motorcycle": ["मोटरसाइकिल", "ಮೋಟಾರ್ ಸೈಕಲ್", "மோட்டார் சைக்கிள்", "మోటార్ సైకిల్"],
    "bus": ["बस", "ಬಸ್", "பேருந்து", "బస్సు"],
    "truck": ["ट्रक", "ಟ್ರಕ್", "லாரி", "ట్రక్"],
    "train": ["ट्रेन", "ರೈಲು", "ரயில்", "రైలు"],
    "airplane": ["हवाई जहाज", "ವಿಮಾನ", "விமானம்", "విమానం"],
    "boat": ["नाव", "ದೋಣಿ", "படகு", "పడవ"],

    "door": ["दरवाज़ा", "ಬಾಗಿಲು", "கதவு", "తలుపు"],
    "window": ["खिड़की", "ಕಿಟಕಿ", "ஜன்னல்", "కిటికీ"],
    "stairs": ["सीढ़ियाँ", "ಮೆಟ್ಟಿಲುಗಳು", "படிக்கட்டுகள்", "మెట్లు"],
    "staircase": ["सीढ़ियाँ", "ಮೆಟ್ಟಿಲುಗಳು", "படிக்கட்டுகள்", "మెట్లు"],
    "wall": ["दीवार", "ಗೋಡೆ", "சுவர்", "గోడ"],
    "floor": ["फर्श", "ನೆಲ", "தரை", "నేల"],
    "ceiling": ["छत", "ಮೇಲ್ಛಾವಣಿ", "கூரை", "పైకప్పు"],
    "door handle": ["दरवाज़े का हैंडल", "ಬಾಗಿಲಿನ ಹಿಡಿ", "கதவு கைப்பிடி", "తలుపు హ్యాండిల్"],

    "chair": ["कुर्सी", "ಕುರ್ಚಿ", "நாற்காலி", "కుర్చీ"],
    "table": ["मेज़", "ಮೇಜು", "மேசை", "బల్ల"],
    "desk": ["डेस्क", "ಡೆಸ್ಕ್", "மேசை", "డెస్క్"],
    "sofa": ["सोफा", "ಸೋಫಾ", "சோபா", "సోఫా"],
    "couch": ["सोफा", "ಸೋಫಾ", "சோபா", "సోఫా"],
    "bed": ["बिस्तर", "ಹಾಸಿಗೆ", "படுக்கை", "మంచం"],
    "bench": ["बेंच", "ಬೆಂಚ್", "பெஞ்ச்", "బెంచ్"],

    "laptop": ["लैपटॉप", "ಲ್ಯಾಪ್‌ಟಾಪ್", "மடிக்கணினி", "ల్యాప్‌టాప్"],
    "computer": ["कंप्यूटर", "ಕಂಪ್ಯೂಟರ್", "கணினி", "కంప్యూటర్"],
    "keyboard": ["कीबोर्ड", "ಕೀಬೋರ್ಡ್", "விசைப்பலகை", "కీబోర్డ్"],
    "mouse": ["माउस", "ಮೌಸ್", "மவுஸ்", "మౌస్"],
    "mobile phone": ["मोबाइल फोन", "ಮೊಬೈಲ್ ಫೋನ್", "கைபேசி", "మొబైల్ ఫోన్"],
    "smartphone": ["स्मार्टफोन", "ಸ್ಮಾರ್ಟ್‌ಫೋನ್", "ஸ்மார்ட்போன்", "స్మార్ట్‌ఫోన్"],
    "tablet": ["टैबलेट", "ಟ್ಯಾಬ್ಲೆಟ್", "டேப்லெட்", "టాబ్లెట్"],
    "television": ["टीवी", "ಟಿವಿ", "தொலைக்காட்சி", "టీవీ"],
    "remote control": ["रिमोट", "ರಿಮೋಟ್", "ரிமோட்", "రిమోట్"],
    "camera": ["कैमरा", "ಕ್ಯಾಮೆರಾ", "கேமரா", "కెమెరా"],
    "speaker": ["स्पीकर", "ಸ್ಪೀಕರ್", "ஸ்பீக்கர்", "స్పీకర్"],
    "headphones": ["हेडफोन", "ಹೆಡ್‌ಫೋನ್", "ஹெட்ஃபோன்", "హెడ్‌ఫోన్స్"],

    "bottle": ["बोतल", "ಬಾಟಲಿ", "பாட்டில்", "బాటిల్"],
    "water bottle": ["पानी की बोतल", "ನೀರಿನ ಬಾಟಲಿ", "தண்ணீர் பாட்டில்", "నీళ్ల బాటిల్"],
    "cup": ["कप", "ಕಪ್", "கோப்பை", "కప్పు"],
    "glass": ["गिलास", "ಗ್ಲಾಸ್", "கண்ணாடி", "గ్లాస్"],
    "plate": ["प्लेट", "ತಟ್ಟೆ", "தட்டு", "ప్లేట్"],
    "bowl": ["कटोरा", "ಬಟ್ಟಲು", "கிண்ணம்", "గిన్నె"],
    "spoon": ["चम्मच", "ಚಮಚ", "கரண்டி", "చెంచా"],
    "fork": ["कांटा", "ಫೋರ್ಕ್", "முள் கரண்டி", "ఫోర్క్"],
    "knife": ["चाकू", "ಚಾಕು", "கத்தி", "కత్తి"],

    "book": ["किताब", "ಪುಸ್ತಕ", "புத்தகம்", "పుస్తకం"],
    "notebook": ["नोटबुक", "ನೋಟ್ಬುಕ್", "நோட்புக்", "నోట్‌బుక్"],
    "pen": ["कलम", "ಪೆನ್", "பேனா", "పెన్"],
    "pencil": ["पेंसिल", "ಪೆನ್ಸಿಲ್", "பென்சில்", "పెన్సిల్"],
    "eraser": ["रबर", "ರಬ್ಬರ್", "அழிப்பான்", "రబ్బరు"],
    "ruler": ["स्केल", "ಸ್ಕೇಲ್", "அளவுகோல்", "స్కేల్"],

    "bag": ["बैग", "ಚೀಲ", "பை", "బ్యాగ్"],
    "backpack": ["बैग", "ಬೆನ್ನುಚೀಲ", "முதுகுப்பை", "బ్యాక్‌ప్యాక్"],
    "handbag": ["हैंडबैग", "ಕೈಚೀಲ", "கைப்பை", "హ్యాండ్‌బ్యాగ్"],
    "suitcase": ["सूटकेस", "ಸೂಟ್‌ಕೇಸ್", "சூட்கேஸ்", "సూట్‌కేస్"],
    "wallet": ["बटुआ", "ಹಣದ ಚೀಲ", "பணப்பை", "పర్సు"],
    "umbrella": ["छाता", "ಛತ್ರಿ", "குடை", "గొడుగు"],

    "shirt": ["कमीज़", "ಅಂಗಿ", "சட்டை", "చొక్కా"],
    "pants": ["पैंट", "ಪ್ಯಾಂಟ್", "கால்சட்டை", "ప్యాంట్"],
    "shoe": ["जूता", "ಶೂ", "காலணி", "చెప్పు"],
    "helmet": ["हेलमेट", "ಹೆಲ್ಮೆಟ್", "தலைக்கவசம்", "హెల్మెట్"],
    "hat": ["टोपी", "ಟೋಪಿ", "தொப்பி", "టోపీ"],
    "tie": ["टाई", "ಟೈ", "டை", "టై"],
    "glasses": ["चश्मा", "ಕನ್ನಡಕ", "கண்ணாடி", "కళ్లద్దాలు"],
    "watch": ["घड़ी", "ಗಡಿಯಾರ", "கைக்கடிகாரம்", "గడియారం"],

    "medicine": ["दवा", "ಔಷಧಿ", "மருந்து", "మందు"],
    "medicine bottle": ["दवा की बोतल", "ಔಷಧಿಯ ಬಾಟಲಿ", "மருந்து பாட்டில்", "మందు బాటిల్"],
    "pill": ["गोली", "ಮಾತ್ರೆ", "மாத்திரை", "మాత్ర"],
    "medical box": ["दवा का डिब्बा", "ಔಷಧಿ ಪೆಟ್ಟಿಗೆ", "மருந்து பெட்டி", "మందుల పెట్టె"],
    "first aid box": ["प्राथमिक उपचार पेटी", "ಪ್ರಥಮ ಚಿಕಿತ್ಸಾ ಪೆಟ್ಟಿಗೆ", "முதலுதவி பெட்டி", "ప్రథమ చికిత్స పెట్టె"],

    "light switch": ["लाइट स्विच", "ಲೈಟ್ ಸ್ವಿಚ್", "விளக்கு சுவிட்ச்", "లైట్ స్విచ్"],
    "electrical socket": ["बिजली का सॉकेट", "ವಿದ್ಯುತ್ ಸಾಕೆಟ್", "மின்சார சாக்கெட்", "ఎలక్ట్రిక్ సాకెట్"],
    "fan": ["पंखा", "ಫ್ಯಾನ್", "மின்விசிறி", "ఫ్యాన్"],
    "refrigerator": ["फ्रिज", "ಫ್ರಿಜ್", "குளிர்சாதன பெட்டி", "ఫ్రిజ్"],
    "microwave": ["माइक्रोवेव", "ಮೈಕ್ರೋವೇವ್", "மைக்ரோவேவ்", "మైక్రోవేవ్"],
    "oven": ["ओवन", "ಓವನ್", "ஓவன்", "ఓవెన్"],
    "toaster": ["टोस्टर", "ಟೋಸ್ಟರ್", "டோஸ்டர்", "టోస్టర్"],
    "sink": ["सिंक", "ಸಿಂಕ್", "தொட்டி", "సింక్"],

    "traffic light": ["ट्रैफिक लाइट", "ಟ್ರಾಫಿಕ್ ಲೈಟ್", "போக்குவரத்து விளக்கு", "ట్రాఫిక్ లైట్"],
    "stop sign": ["स्टॉप साइन", "ನಿಲ್ಲುವ ಸೂಚನಾ ಫಲಕ", "நிறுத்த குறியீடு", "స్టాప్ సైన్"],
    "fire hydrant": ["फायर हाइड्रेंट", "ಅಗ್ನಿಶಾಮಕ ನೀರಿನ ಕವಾಟ", "தீயணைப்பு நீர்க்குழாய்", "ఫైర్ హైడ్రెంట్"],
    "parking meter": ["पार्किंग मीटर", "ಪಾರ್ಕಿಂಗ್ ಮೀಟರ್", "வாகன நிறுத்த மீட்டர்", "పార్కింగ్ మీటర్"],

    "dog": ["कुत्ता", "ನಾಯಿ", "நாய்", "కుక్క"],
    "cat": ["बिल्ली", "ಬೆಕ್ಕು", "பூனை", "పిల్లి"],
    "bird": ["पक्षी", "ಪಕ್ಷಿ", "பறவை", "పక్షి"],
    "horse": ["घोड़ा", "ಕುದುರೆ", "குதிரை", "గుర్రం"],
    "cow": ["गाय", "ಹಸು", "மாடு", "ఆవు"],
    "sheep": ["भेड़", "ಕುರಿ", "செம்மறியாடு", "గొర్రె"],
    "elephant": ["हाथी", "ಆನೆ", "யானை", "ఏనుగు"],
    "bear": ["भालू", "ಕರಡಿ", "கரடி", "ఎలుగుబంటి"],
    "zebra": ["ज़ेब्रा", "ಜೀಬ್ರಾ", "வரிக்குதிரை", "జీబ్రా"],
    "giraffe": ["जिराफ", "ಜಿರಾಫೆ", "ஒட்டகச்சிவிங்கி", "జిరాఫీ"],

    "tree": ["पेड़", "ಮರ", "மரம்", "చెట్టు"],
    "plant": ["पौधा", "ಗಿಡ", "செடி", "మొక్క"],
    "flower": ["फूल", "ಹೂವು", "மலர்", "పువ్వు"],
    "potted plant": ["गमले का पौधा", "ಕುಂಡದ ಗಿಡ", "தொட்டிச் செடி", "కుండ మొక్క"],

    "food": ["खाना", "ಆಹಾರ", "உணவு", "ఆహారం"],
    "pizza": ["पिज़्ज़ा", "ಪಿಜ್ಜಾ", "பீட்சா", "పిజ్జా"],
    "cake": ["केक", "ಕೇಕ್", "கேக்", "కేక్"],
    "apple": ["सेब", "ಸೇಬು", "ஆப்பிள்", "ఆపిల్"],
    "banana": ["केला", "ಬಾಳೆಹಣ್ಣು", "வாழைப்பழம்", "అరటిపండు"],
    "orange": ["संतरा", "ಕಿತ್ತಳೆ", "ஆரஞ்சு", "నారింజ"],
    "sandwich": ["सैंडविच", "ಸ್ಯಾಂಡ್‌ವಿಚ್", "சாண்ட்விச்", "శాండ్‌విచ్"],

    "scissors": ["कैंची", "ಕತ್ತರಿ", "கத்தரிக்கோல்", "కత్తెర"],
    "teddy bear": ["टेडी बियर", "ಟೆಡ್ಡಿ ಬೇರ್", "டெடி பியர்", "టెడ్డి బేర్"],
    "toothbrush": ["टूथब्रश", "ಹಲ್ಲುಜ್ಜುವ ಬ್ರಷ್", "பல் துலக்கி", "టూత్‌బ్రష్"],
    "hair dryer": ["हेयर ड्रायर", "ಹೇರ್ ಡ್ರೈಯರ್", "முடி உலர்த்தி", "హెయిర్ డ్రయ్యర్"],
    "key": ["चाबी", "ಕೀಲಿ", "சாவி", "తాళంచెవి"],
    "money": ["पैसे", "ಹಣ", "பணம்", "డబ్బు"]
}


# ============================================================
# POSITION TRANSLATIONS
# ============================================================

POSITION_TRANSLATIONS = {

    "left": {
        "en": "on your left",
        "hi": "आपकी बाईं ओर",
        "kn": "ನಿಮ್ಮ ಎಡಭಾಗದಲ್ಲಿ",
        "ta": "உங்கள் இடப்புறத்தில்",
        "te": "మీ ఎడమ వైపున"
    },

    "right": {
        "en": "on your right",
        "hi": "आपकी दाईं ओर",
        "kn": "ನಿಮ್ಮ ಬಲಭಾಗದಲ್ಲಿ",
        "ta": "உங்கள் வலப்புறத்தில்",
        "te": "మీ కుడి వైపున"
    },

    "ahead": {
        "en": "ahead",
        "hi": "सामने",
        "kn": "ಮುಂದೆ",
        "ta": "முன்னால்",
        "te": "ముందు"
    }
}


# ============================================================
# DISTANCE TRANSLATIONS
# ============================================================

DISTANCE_TRANSLATIONS = {

    "very close": {
        "en": "very close",
        "hi": "बहुत पास",
        "kn": "ತುಂಬಾ ಹತ್ತಿರ",
        "ta": "மிகவும் அருகில்",
        "te": "చాలా దగ్గరగా"
    },

    "near": {
        "en": "near",
        "hi": "पास",
        "kn": "ಹತ್ತಿರ",
        "ta": "அருகில்",
        "te": "దగ్గరగా"
    },

    "far": {
        "en": "far",
        "hi": "दूर",
        "kn": "ದೂರ",
        "ta": "தொலைவில்",
        "te": "దూరంగా"
    }
}


# ============================================================
# SPEECH QUEUE
# ============================================================

speech_queue = queue.Queue(maxsize=1)

stop_signal = threading.Event()


def clear_speech_queue():

    while not speech_queue.empty():

        try:

            speech_queue.get_nowait()
            speech_queue.task_done()

        except queue.Empty:

            break


def speak(message):

    clear_speech_queue()

    try:

        speech_queue.put_nowait(message)

    except queue.Full:

        pass


# ============================================================
# TEXT TO SPEECH WORKER
# ============================================================

def tts_worker():

    try:

        pygame.mixer.init()

    except Exception as e:

        print("Audio initialization error:", e)

        return


    while not stop_signal.is_set():

        try:

            message = speech_queue.get(timeout=0.1)

        except queue.Empty:

            continue


        if message is None:

            try:
                speech_queue.task_done()
            except:
                pass

            break


        # IMPORTANT:
        # Use a unique MP3 file every time.
        # This fixes Windows "Permission denied" errors.
        audio_file = (
            f"see_for_all_{time.time_ns()}.mp3"
        )


        try:

            print("Speaking:", message)


            # Generate speech
            tts = gTTS(
                text=message,
                lang=LANGUAGE,
                slow=False
            )


            tts.save(audio_file)


            # Stop if Q/ESC was pressed
            if stop_signal.is_set():

                break


            # Load audio
            pygame.mixer.music.load(
                audio_file
            )


            # Play audio
            pygame.mixer.music.play()


            # Wait while audio is playing
            while pygame.mixer.music.get_busy():

                if stop_signal.is_set():

                    pygame.mixer.music.stop()

                    break

                time.sleep(0.05)


            # Release MP3 file
            try:

                pygame.mixer.music.unload()

            except:

                pass


        except Exception as e:

            print(
                "TTS error:",
                e
            )


        finally:

            # Delete temporary MP3
            try:

                if os.path.exists(audio_file):

                    os.remove(audio_file)

            except Exception as e:

                print(
                    "Could not delete audio file:",
                    e
                )


        try:

            speech_queue.task_done()

        except:

            pass


    # Final audio cleanup
    try:

        pygame.mixer.music.stop()

        try:

            pygame.mixer.music.unload()

        except:

            pass

        pygame.mixer.quit()

    except:

        pass


# ============================================================
# POSITION DETECTION
# ============================================================

def get_position(
    center_x,
    frame_width
):

    left_limit = frame_width / 3

    right_limit = frame_width * 2 / 3


    if center_x < left_limit:

        return "left"


    elif center_x > right_limit:

        return "right"


    else:

        return "ahead"


# ============================================================
# APPROXIMATE DISTANCE
# ============================================================

def estimate_distance(
    box_height,
    frame_height
):

    ratio = box_height / frame_height


    if ratio > 0.45:

        return "very close"


    elif ratio > 0.25:

        return "near"


    else:

        return "far"


# ============================================================
# TRANSLATE OBJECT
# ============================================================

def translate_object(object_name):

    # English
    if LANGUAGE == "en":

        return object_name


    # Check translation dictionary
    if object_name in TRANSLATIONS:

        language_index = {

            "hi": 0,
            "kn": 1,
            "ta": 2,
            "te": 3

        }.get(LANGUAGE)


        if language_index is not None:

            return TRANSLATIONS[
                object_name
            ][language_index]


    # Fallback
    return object_name


# ============================================================
# CREATE SPOKEN SENTENCE
# ============================================================

def create_sentence(
    object_name,
    position,
    distance
):

    translated_object = translate_object(
        object_name
    )


    translated_position = (
        POSITION_TRANSLATIONS[position]
        .get(
            LANGUAGE,
            position
        )
    )


    translated_distance = (
        DISTANCE_TRANSLATIONS[distance]
        .get(
            LANGUAGE,
            distance
        )
    )


    return (
        f"{translated_object} "
        f"{translated_position}, "
        f"{translated_distance}"
    )


# ============================================================
# LOAD YOLO-WORLD
# ============================================================

print("Loading YOLO-World...")

try:

    model = YOLOWorld(
        "yolov8s-worldv2.pt"
    )

except Exception as e:

    print()
    print("ERROR loading YOLO-World:")
    print(e)
    print()
    print(
        "Make sure Ultralytics is installed:"
    )
    print(
        "pip install -U ultralytics"
    )

    raise SystemExit


print("Setting object vocabulary...")

try:

    model.set_classes(
        OBJECTS
    )

except Exception as e:

    print()
    print("ERROR setting object vocabulary:")
    print(e)
    print()

    raise SystemExit


print("YOLO-World ready.")


# ============================================================
# START SPEECH THREAD
# ============================================================

speech_thread = threading.Thread(
    target=tts_worker,
    daemon=True
)

speech_thread.start()


# ============================================================
# START CAMERA
# ============================================================

cap = cv2.VideoCapture(0)


if not cap.isOpened():

    print(
        "ERROR: Could not open webcam."
    )

    stop_signal.set()

    raise SystemExit


# ============================================================
# START MESSAGE
# ============================================================

print()
print("========================================")
print("          SEE FOR ALL - STARTED")
print("========================================")
print()
print(
    "Language:",
    LANGUAGE
)
print()
print(
    "Press Q or ESC to stop."
)
print()


# ============================================================
# VARIABLES
# ============================================================

last_scene = set()

last_speech_time = 0

last_refresh_time = 0


# ============================================================
# MAIN LOOP
# ============================================================

try:

    while not stop_signal.is_set():

        # --------------------------------------------
        # READ CAMERA
        # --------------------------------------------

        ret, frame = cap.read()


        if not ret:

            print(
                "Could not read webcam frame."
            )

            break


        # --------------------------------------------
        # YOLO-WORLD DETECTION
        # --------------------------------------------

        results = model(
            frame,
            conf=CONF_THRESH,
            verbose=False
        )


        current_objects = []

        current_scene = set()


        # --------------------------------------------
        # PROCESS DETECTIONS
        # --------------------------------------------

        for result in results:

            boxes = result.boxes


            for box in boxes:

                confidence = float(
                    box.conf[0]
                )


                if confidence < CONF_THRESH:

                    continue


                # Bounding box
                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                # Class ID
                class_id = int(
                    box.cls[0]
                )


                # Object name
                object_name = model.names[
                    class_id
                ]


                # Center of object
                center_x = int(
                    (x1 + x2) / 2
                )


                # Position
                position = get_position(
                    center_x,
                    frame.shape[1]
                )


                # Approximate distance
                box_height = y2 - y1


                distance = estimate_distance(
                    box_height,
                    frame.shape[0]
                )


                # Create translated sentence
                sentence = create_sentence(
                    object_name,
                    position,
                    distance
                )


                current_objects.append(
                    sentence
                )


                current_scene.add(
                    (
                        object_name,
                        position,
                        distance
                    )
                )


                # ------------------------------------
                # DRAW BOUNDING BOX
                # ------------------------------------

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )


                # Label
                label = (
                    f"{object_name} "
                    f"{confidence:.2f}"
                )


                cv2.putText(
                    frame,
                    label,
                    (
                        x1,
                        max(
                            y1 - 10,
                            20
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )


        # ====================================================
        # SPEECH CONTROL
        # ====================================================

        current_time = time.time()


        scene_changed = (
            current_scene != last_scene
        )


        refresh_required = (
            current_time
            - last_refresh_time
            >= REFRESH_INTERVAL
        )


        enough_time_passed = (
            current_time
            - last_speech_time
            >= SPEAK_INTERVAL
        )


        if current_objects:

            if (
                scene_changed
                or (
                    refresh_required
                    and enough_time_passed
                )
            ):

                # Remove duplicate sentences
                unique_objects = list(
                    dict.fromkeys(
                        current_objects
                    )
                )


                # Speak maximum 4 objects
                unique_objects = (
                    unique_objects[:4]
                )


                # Combine sentences
                message = ". ".join(
                    unique_objects
                )


                print(
                    "Speaking:",
                    message
                )


                speak(message)


                last_speech_time = (
                    current_time
                )


                last_refresh_time = (
                    current_time
                )


        # Save current scene
        last_scene = current_scene


        # ====================================================
        # DISPLAY LANGUAGE
        # ====================================================

        language_names = {

            "en": "English",
            "hi": "Hindi",
            "kn": "Kannada",
            "ta": "Tamil",
            "te": "Telugu"

        }


        language_name = language_names.get(
            LANGUAGE,
            LANGUAGE
        )


        cv2.putText(
            frame,
            f"Language: {language_name}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            "Q / ESC = EXIT",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        # ====================================================
        # SHOW CAMERA
        # ====================================================

        cv2.imshow(
            "SeeForAll - YOLO World",
            frame
        )


        # ====================================================
        # KEYBOARD CONTROL
        # ====================================================

        key = cv2.waitKey(1) & 0xFF


        # Q
        if key == ord("q"):

            print(
                "Q pressed. Stopping..."
            )

            break


        # Q uppercase
        if key == ord("Q"):

            print(
                "Q pressed. Stopping..."
            )

            break


        # ESC
        if key == 27:

            print(
                "ESC pressed. Stopping..."
            )

            break


# ============================================================
# CLEANUP
# ============================================================

finally:

    print()
    print("Cleaning up...")


    # Tell speech thread to stop
    stop_signal.set()


    # Clear waiting speech
    clear_speech_queue()


    # Stop audio
    try:

        pygame.mixer.music.stop()

    except:

        pass


    # Release webcam
    try:

        cap.release()

    except:

        pass


    # Close OpenCV window
    cv2.destroyAllWindows()


    print(
        "SeeForAll stopped."
    )