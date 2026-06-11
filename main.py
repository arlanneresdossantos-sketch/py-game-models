import json
import init_django_orm  # noqa: F401

from db.models import Race, Skill, Guild, Player


def main() -> None:
    # 1. Read data from the JSON file
    with open("players.json", "r") as file:
        players_data = json.load(file)

    # 2. Iterate and seamlessly populate the database
    for player_name, data in players_data.items():
        # Get or create the Race
        race, _ = Race.objects.get_or_create(
            name=data["race"]["name"],
            defaults={"description": data["race"].get("description")}
        )

        # Get or create the Race's Skills
        for skill_data in data["race"].get("skills", []):
            Skill.objects.get_or_create(
                name=skill_data["name"],
                defaults={
                    "bonus": skill_data["bonus"],
                    "race": race
                }
            )

        # Get or create the Guild (if the player has one)
        guild = None
        if data.get("guild"):
            guild, _ = Guild.objects.get_or_create(
                name=data["guild"]["name"],
                defaults={"description": data["guild"].get("description")}
            )

        # Create or update the Player
        Player.objects.get_or_create(
            nickname=player_name,
            defaults={
                "email": data["email"],
                "bio": data["bio"],
                "race": race,
                "guild": guild
            }
        )

if __name__ == "__main__":
    main()
