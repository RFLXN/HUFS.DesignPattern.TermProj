class PathLikeDict(dict):
    def __truediv__(self, other: str):
        return self.get(other)
