class Window(object):
    def __init__(self, timestamp, seen_count):
        self.timestamp = timestamp
        self.seen_count = seen_count

    def __eq__(self, other) -> bool:
        if not isinstance(other, Window):
            return False
        return self.timestamp == other.timestamp

    def __hash__(self) -> int:
        return hash(self.timestamp)

    def __str__(self) -> str:
        return "{ " + f"time: {self.timestamp}, seen: {self.seen_count}" + " }"


class CampaignWindowPair(object):
    def __init__(self, campaign, window: Window):
        self.campaign = campaign
        self.window = window

    def __eq__(self, other) -> bool:
        if not isinstance(other, CampaignWindowPair):
            return False
        return (
            self.campaign == other.campaign
            and self.window.timestamp == other.window.timestamp
        )

    def __hash__(self) -> int:
        prime = 31
        result = 1
        result = result * prime + hash(self.campaign)
        result = result * prime + hash(self.window.timestamp)
        return result

    def __str__(self) -> str:
        return "{ " + f"{self.campaign} : {self.window}" + " }"


if __name__ == "__main__":
    w = Window("123123", 2)
    print(w)
    campaign = "alibaba"

    pair = CampaignWindowPair(campaign, w)
    print(pair)
    pair.window.seen_count += 1
    print(pair)
