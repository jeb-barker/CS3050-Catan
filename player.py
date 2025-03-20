from texture_enums import Resource

class Player:
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color

    # Dictionary to track resources
        self.resources = {resource: 0 for resource in Resource}

    def remove_resource(self, resource):
        if self.resources[resource] > 0:
            self.resources[resource] -= 1
        else:
            print(f"Not enough {resource.name} to remove.")