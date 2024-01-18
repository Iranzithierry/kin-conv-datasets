import re
NOISE = [
    "Liked a message",
    "sent an attachment",
    "You sent an attachment.",
    "liked a message" "shared a story",
    "changed the theme",
    "can now message and call",
    "missed a",
    "wasn't notified about this message",
    "You are now connected on Messenger",
    "missed your call",
    "You started a video chat",
    "You started an audio call",
    "Audio call ended",
    "Video chat ended",
    "You set the quick reaction to",
]
def remove_noise(message):
    for noise in NOISE:
        message = re.sub(
                rf"\b{re.escape(noise)}\b", "", message, flags=re.IGNORECASE
        )
    return message

print(remove_noise("Hello You are now [vp] connected on Messenger Audio call ended"))