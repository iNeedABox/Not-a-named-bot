from flask import Flask, jsonify

app = Flask(__name__)

slurs = [
    "fuck", "nigger", "porn",
    "dick", "pennis", "slur",
    "swear", "cock", "dick",
    "imbécil", "idiota", "hijo de puta",
    "masturbate", "masturbarse", "eyacular",
    "eyacularse", "joder", "me cago en",
    "fuck it", "fuck you", "fuck me",
    "shit", "badass", "baddies",
    "monkey ahh", "ugly", "suck",
    "donkey", "you're ugly", "you stink",
    "i'm tolerant", "sex", "hitler",
    "Jebi se", "ejaculate", "Puši kurac",
    "Jebem pas mater", "Koj si ti retard"
]

@app.route("/", methods=["GET"])
def get_slurs():
    return jsonify(slurs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)