import CrowdAnki.utils
from CrowdAnki.note import Note
from CrowdAnki.json_serializable import JsonSerializable

UUID_FIELD_NAME = "crowdanki_uuid"


class Deck(JsonSerializable):
    filter_set = {"anki_deck", "collection"}

    def __init__(self):
        self.collection = None
        self.name = None
        self.anki_deck = None
        self.notes = None
        self.children = None

    @classmethod
    def from_collection(cls, collection, name):
        deck = Deck()
        deck.collection = collection
        deck.name = name

        deck.update_db()
        deck.anki_deck = collection.decks.byName(name)

        deck.notes = Note.get_notes_from_collection(collection, deck.anki_deck["id"])  # Todo ugly

        deck.children = [cls.from_collection(collection, child_name) for child_name, _ in
                         collection.decks.children(deck.anki_deck["id"])]

        return deck

    def update_db(self):
        # Introduce uuid field for unique identification of entities
        CrowdAnki.utils.add_column(self.collection.db, "notes", UUID_FIELD_NAME)

    def _dict_extension(self):
        return self.anki_deck