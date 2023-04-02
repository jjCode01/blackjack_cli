class Card:
    """A class to represent a playing card"""

    def __init__(self, face, suit, value=0, face_down=False):
        self.face = face
        self.suit = suit
        self.value = value
        self.face_down = face_down

    def __str__(self) -> str:
        return f"{self.face}-{self.suit[0]}"

    def flip(self):
        """Flip card to be face down or face up"""
        self.face_down = not self.face_down
