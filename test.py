from pypad.active_skill.active_skills import ActiveSkills
from pypad.card.cards import Cards
from pypad.region import Region
from pypad.awakening import Awakening
from pypad.latent_awakening import LatentAwakening
from pypad.data import update_game_files

#update_game_files()
cards = Cards(Region.NA)

for card in cards:
    if 'goblin' in card.name.lower():
        print(f'G[{card.id}] {card.name} -> size: {card.size}')