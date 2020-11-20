
class CompendiumLink:
    """An abstraction to handle pointers from one compendium to another that waits
       to resolve (stored by key). This allows us to reload compendiums and the
       link points to the new compendium."""

    def __init__(self, compendiums: dict, key: str):
        self.compendiums = compendiums
        self.key = key

    @property
    def ref(self):
        return self.compendiums[self.key]
