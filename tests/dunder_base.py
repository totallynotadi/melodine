class URIBase:

    uri = repr(None)

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, __o: object) -> bool:
        return (
            type(self) is type(__o) and self.uri == __o.uri
        )
    
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __str__(self) -> str:
        return self.uri

class TestTrack(URIBase):
    def __init__(self, uri) -> None:
        self.uri = uri

if __name__ == "__main__":
    track_one = TestTrack('str_one')
    track_two = TestTrack('str_two')

    print(track_one != track_two)

