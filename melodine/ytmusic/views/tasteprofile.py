from dataclasses import dataclass

from melodine.services import service


@dataclass
class ProfileData:
    selection_value: str
    impression_value: str


@dataclass
class TasteProfile:
    artist: str
    profile_data: ProfileData


def get_tasteprofiles():
    tasteprofiles = service.ytmusic.get_tasteprofile()
    tasteprofiles = list(tasteprofiles.items())
    return list(
        map(
            lambda x: TasteProfile(
                x[0],
                ProfileData(x[1]),
            ),
            tasteprofiles,
        )
    )
