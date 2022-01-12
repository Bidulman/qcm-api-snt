from .possibility import Possibility


class Possibilities(list[Possibility]):

    def from_json(self, possibilities: []):
        iterations = 1
        for json_possibility in possibilities:
            object_possibility = Possibility(iterations)
            object_possibility.from_json(json_possibility)
            self.append(object_possibility)
            iterations += 1
        return self
