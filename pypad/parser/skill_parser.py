from .json_parser import JsonParser
from .common import convert, all_attr, multiplier, defaultlist, cc, single_to_list, collection_to_list, binary_to_list, unimplimented, increase_multiplier, list_of_binary_to_list, positive_values_to_list
from collections import defaultdict

_passive_stats_defaults = {'for_attr': [], 'for_type': [], 'hp_multiplier': 1.0, 'atk_multiplier': 1.0, 'rcv_multiplier': 1.0, 'reduction_attributes': all_attr, 'damage_reduction': 0.0}   
def _passive_stats_convert(arguments):
    return convert('passive_stats', {k:(arguments[k] if k in arguments else v) for k,v in _passive_stats_defaults.items()})

_threshold_stats_defaults = {'for_attr': [], 'for_type': [], 'threshold': False, 'atk_multiplier': 1.0, 'rcv_multiplier': 1.0, 'reduction_attributes': all_attr, 'damage_reduction': 0.0}
_ABOVE = True
_BELOW = False
def _threshold_stats_convert(above, arguments):
    if above:
        return convert('above_threshold_stats', {k:(arguments[k] if k in arguments else v) for k,v in _threshold_stats_defaults.items()})
    else:
        return convert('below_threshold_stats', {k:(arguments[k] if k in arguments else v) for k,v in _threshold_stats_defaults.items()})

_combo_match_defaults = {'for_attr': [], 'for_type': [], 'minimum_combos': 0, 'minimum_atk_multiplier': 1.0, 'minimum_rcv_multiplier': 1.0, 'minimum_damage_reduction': 0.0,
                                                                            'bonus_atk_multiplier': 0.0,   'bonus_rcv_multiplier': 0.0,   'bonus_damage_reduction': 0.0,
                                                       'maximum_combos': 0, 'reduction_attributes': all_attr}
def _combo_match_convert(arguments):
    def f(x):
        _,c = convert('combo_match', {k:(arguments[k] if k in arguments else v) for k,v in _combo_match_defaults.items()})(x)
        if c['maximum_combos'] == 0:
            c['maximum_combos'] = c['minimum_combos']
        return 'combo_match',c
    return f

_attribute_match_defaults = {'attributes': [], 'minimum_attributes': 0, 'minimum_atk_multiplier': 1.0, 'minimum_rcv_multiplier': 1.0, 'minimum_damage_reduction': 0.0,
                                                                      'bonus_atk_multiplier': 0.0,   'bonus_rcv_multiplier': 0.0,   'bonus_damage_reduction': 0.0,
                                             'maximum_attributes': 0, 'reduction_attributes': all_attr}   
def _attribute_match_convert(arguments):
    def f(x):
        _,c = convert('attribute_match', {k:(arguments[k] if k in arguments else v) for k,v in _attribute_match_defaults.items()})(x)
        if c['maximum_attributes'] == 0:
            c['maximum_attributes'] = c['minimum_attributes']
        return 'attribute_match',c
    return f
_multi_attribute_match_defaults = {'attributes': [], 'minimum_match': 0, 'minimum_atk_multiplier': 1.0, 'minimum_rcv_multiplier': 1.0, 'minimum_damage_reduction': 0.0,
                                                                       'bonus_atk_multiplier': 0.0,   'bonus_rcv_multiplier': 0.0,   'bonus_damage_reduction': 0.0,
                                                   'reduction_attributes': all_attr}   
def _multi_attribute_match_convert(arguments):
    return convert('multi-attribute_match', {k:(arguments[k] if k in arguments else v) for k,v in _multi_attribute_match_defaults.items()})

_mass_match_defaults = {'attributes': [], 'minimum_count': 0, 'minimum_atk_multiplier': 1.0, 'minimum_rcv_multiplier': 1.0, 'minimum_damage_reduction': 0.0,
                                                            'bonus_atk_multiplier': 0.0,   'bonus_rcv_multiplier': 0.0,   'bonus_damage_reduction': 0.0,
                                        'maximum_count': 0, 'reduction_attributes': all_attr}   
def _mass_match_convert(arguments):
    def f(x):
        _,c = convert('mass_match', {k:(arguments[k] if k in arguments else v) for k,v in _mass_match_defaults.items()})(x)
        if c['maximum_count'] == 0:
            c['maximum_count'] = c['minimum_count']
        return 'mass_match',c
    return f

_atk_from_slice = lambda x: multiplier(x[2]) if 1 in x[:2] else 1.0
_rcv_from_slice = lambda x: multiplier(x[2]) if 2 in x[:2] else 1.0


class SkillParser(JsonParser):
    _skills = {
          0: lambda x: \
          convert('null_skill', {})(x) \
          if defaultlist(int,x)[1] == 0 else \
          convert('attack_attr_x_atk', {'attribute': (0,cc), 'multiplier': (1,multiplier), 'mass_attack': True})(x),
          1: convert('attack_attr_damage', {'attribute': (0,cc), 'damage': (1,cc), 'mass_attack': True}),
          2: convert('attack_x_atk', {'multiplier': (0,multiplier), 'mass_attack': False}),
          3: convert('damage_shield_buff', {'duration': (0,cc), 'reduction': (1,multiplier)}),
          4: convert('poison', {'multiplier': (0,multiplier)}),
          5: convert('change_the_world', {'duration': (0,cc)}),
          6: convert('gravity', {'percentage_hp': (0,multiplier)}),
          7: convert('heal_active', {'rcv_multiplier_as_hp': (0,multiplier), 'card_bind': 0, 'hp': 0, 'percentage_max_hp': 0.0, 'awoken_bind': 0, 'team_rcv_multiplier_as_hp': 0.0}),
          8: convert('heal_active', {'hp': (0,cc), 'card_bind': 0, 'rcv_multiplier_as_hp': 0.0, 'percentage_max_hp': 0.0, 'awoken_bind': 0, 'team_rcv_multiplier_as_hp': 0.0}),
          9: convert('single_orb_change', {'from': (0,cc), 'to': (0,cc)}),
         10: convert('board_refresh', {}),
         18: convert('delay', {'turns': (0,cc)}),
         19: convert('defense_reduction', {'duration': (0,cc), 'reduction': (1,multiplier)}),
         20: convert('double_orb_change', {'from_1': (0,cc), 'to_1': (1,cc), 'from_2': (2,cc), 'to_2': (3,cc)}),
         21: convert('elemental_shield_buff', {'duration': (0,cc), 'attribute': (1,cc), 'reduction': (2,multiplier)}),
         35: convert('drain_attack', {'atk_multiplier': (0,multiplier), 'recover_multiplier': (1,multiplier), 'mass_attack': False}),
         37: convert('attack_attr_x_atk', {'attribute': (0,cc), 'multiplier': (1,multiplier), 'mass_attack': False}),
         42: convert('element_attack_attr_damage', {'enemy_attribute': (0,cc), 'attack_attribute':(1,cc) , 'damage': (2,cc)}),
         50: lambda x: \
         convert('rcv_boost', {'duration': (0,cc), 'multiplier': (2,multiplier)})(x) \
         if defaultlist(int,x)[1] == 5 else \
         convert('attribute_attack_boost', {'duration': (0,cc), 'attributes': (1,single_to_list), 'multiplier': (2,multiplier)})(x),
         51: convert('force_mass_attack', {'duration': (0,cc)}),
         52: convert('enhance_orbs', {'orbs': (0,single_to_list)}),
         55: convert('laser', {'damage': (0,cc), 'mass_attack': False}),
         56: convert('laser', {'damage': (0,cc), 'mass_attack': True}),
         58: convert('attack_attr_random_x_atk', {'attribute': (0,cc), 'minimum_multiplier': (1,multiplier), 'maximum_multiplier': (2,multiplier), 'mass_attack': True}),
         59: convert('attack_attr_random_x_atk', {'attribute': (0,cc), 'minimum_multiplier': (1,multiplier), 'maximum_multiplier': (2,multiplier), 'mass_attack': False}),
         60: convert('counter_attack_buff', {'duration': (0,cc), 'multiplier': (1,multiplier), 'attribute': (2,cc)}),
         71: convert('board_change', {'attributes': (slice(None),lambda x: [v for v in x if v != -1])}),
         84: convert('suicide_attack_attr_random_x_atk', {'attribute': (0,cc), 'minimum_multiplier': (1,multiplier), 'maximum_multiplier': (2,multiplier), 'hp_remaining': (3,multiplier), 'mass_attack': False}),
         85: convert('suicide_attack_attr_random_x_atk', {'attribute': (0,cc), 'minimum_multiplier': (1,multiplier), 'maximum_multiplier': (2,multiplier), 'hp_remaining': (3,multiplier), 'mass_attack': True}),
         86: convert('suicide_attack_attr_damage', {'attribute': (0,cc), 'damage': (1,multiplier), 'hp_remaining': (3,multiplier), 'mass_attack': False}),
         87: convert('suicide_attack_attr_damage', {'attribute': (0,cc), 'damage': (1,multiplier), 'hp_remaining': (3,multiplier), 'mass_attack': True}),
         88: convert('type_attack_boost', {'duration': (0,cc), 'types': (1,single_to_list), 'multiplier': (2,multiplier)}),
         90: convert('attribute_attack_boost', {'duration': (0,cc), 'attributes': (slice(1,3),collection_to_list), 'multiplier': (2,multiplier)}),
         91: convert('enhance_orbs', {'orbs': (slice(0,2), collection_to_list)}),
         92: convert('type_attack_boost', {'duration': (0,cc), 'types': (slice(1,3),collection_to_list), 'multiplier': (2,multiplier)}),
         93: convert('leader_swap', {}),
        110: convert('grudge_strike', {'mass_attack': (0,lambda x: x == 0), 'attribute': (1,cc), 'high_multiplier': (2,multiplier), 'low_multiplier': (3,multiplier)}),
        115: convert('drain_attack_attr', {'attribute': (0,cc),'atk_multiplier': (1,multiplier), 'recover_multiplier': (2,multiplier), 'mass_attack': False}),
        116: convert('combine_active_skills', {'skill_ids': (slice(None),collection_to_list)}),
        117: convert('heal_active', {'card_bind': (0,cc), 'rcv_multiplier_as_hp': (1,multiplier), 'hp': (2,cc), 'percentage_max_hp': (3,multiplier), 'awoken_bind': (4,cc), 'team_rcv_multiplier_as_hp': 0.0}),
        118: convert('random_skill', {'skill_ids': (slice(None),collection_to_list)}),
        126: convert('change_skyfall', {'orbs': (0,binary_to_list), 'duration': (1,cc), 'percentage': (3,multiplier)}),
        127: convert('column_change', {'columns': (slice(None),lambda x: [{'index':i if i < 3 else i-6,'orbs':binary_to_list(orbs)} for indices,orbs in zip(x[::2],x[1::2]) for i in binary_to_list(indices)])}), # 0 1 2 -3 -2 -1
        128: convert('row_change', {'rows': (slice(None),lambda x: [{'index':i if i < 2 else i-5,'orbs':binary_to_list(orbs)} for indices,orbs in zip(x[::2],x[1::2]) for i in binary_to_list(indices)])}), # 0 1 -3 -2 -1
        132: convert('move_time_buff', {'duration': (0,cc), 'static': (1,lambda x: x/10), 'percentage': (2,multiplier)}),
        140: convert('enhance_orbs', {'orbs': (0,binary_to_list)}),
        141: convert('spawn_orbs', {'amount': (0,cc), 'orbs': (1,binary_to_list), 'excluding_orbs': (2, binary_to_list)}),
        142: convert('attribute_change', {'duration': (0,cc), 'attribute': (1,cc)}),
        144: convert('attack_attr_x_team_atk', {'team_attributes': (0,binary_to_list), 'multiplier': (1,multiplier), 'mass_attack': (2,lambda x: x == 0), 'attack_attribute': (3,cc),}),
        145: convert('heal_active', {'team_rcv_multiplier_as_hp': (0,multiplier), 'card_bind': 0, 'rcv_multiplier_as_hp': 0.0, 'hp': 0, 'percentage_max_hp': 0.0, 'awoken_bind': 0}),
        146: convert('haste', {'minimum_turns': (0,cc), 'maximum_turns': (1,cc)}),
        152: convert('lock_orbs', {'orbs': (0,binary_to_list)}),
        153: convert('change_enemies_attribute', {'attribute': (0,cc)}),
        154: convert('random_orb_change', {'from': (0,binary_to_list), 'to': (1,binary_to_list)}),
        156: lambda x: \
        convert('awakening_heal', {'duration': (0,cc), 'awakenings': (slice(1,4),collection_to_list), 'amount_per': (5,cc)})(x) \
        if defaultlist(int,x)[4] == 1 else \
        ( convert('awakening_attack_boost', {'duration': (0,cc), 'awakenings': (slice(1,4),collection_to_list), 'amount_per': (5,lambda x: (x - 100) / 100)})(x) \
        if defaultlist(int,x)[4] == 2 else \
        ( convert('awakening_shield', {'duration': (0,cc), 'awakenings': (slice(1,4),collection_to_list), 'amount_per': (5,multiplier)})(x) \
        if defaultlist(int,x)[4] == 3 else \
        ( unimplimented(156)(x) ) ) ),
        160: convert('extra_combo', {'duration': (0,cc), 'combos': (1,cc)}),
        161: convert('true_gravity', {'percentage_max_hp': (0,multiplier)}),
        172: convert('unlock', {}),
        173: convert('absorb_mechanic_void', {'duration': (0,cc), 'attribute_absorb': (1,bool), 'damage_absorb': (3,bool)}),
        179: convert('auto_heal_buff', {'duration': (0,cc), 'percentage_max_hp': (2,multiplier)}),
        180: convert('enhanced_skyfall_buff', {'duration': (0,cc), 'percentage_increase': (1,multiplier)}),
        184: convert('no_skyfall_buff', {'duration': (0,cc)}),
        188: convert('multihit_laser', {'damage': (0,cc), 'mass_attack': False}),
         11: _passive_stats_convert({'for_attr': (0,single_to_list), 'atk_multiplier': (1,multiplier)}),
         12: convert('after_attack_on_match', {'multiplier': (0,multiplier)}),
         13: convert('heal_on_match', {'multiplier': (0,multiplier)}),
         14: convert('resolve', {'threshold': (0,multiplier)}),
         15: convert('bonus_move_time', {'time': (0,multiplier), 'for_attr': [], 'for_type': [], 'hp_multiplier': 1.0, 'atk_multiplier': 1.0, 'rcv_multiplier': 1.0}),
         16: _passive_stats_convert({'reduction_attributes': all_attr, 'damage_reduction': (0,multiplier)}),
         17: _passive_stats_convert({'reduction_attributes': (0,single_to_list), 'damage_reduction': (1,multiplier)}),
         22: _passive_stats_convert({'for_type': (0,single_to_list), 'atk_multiplier': (1,multiplier)}),
         23: _passive_stats_convert({'for_type': (0,single_to_list), 'hp_multiplier': (1,multiplier)}),
         24: _passive_stats_convert({'for_type': (0,single_to_list), 'rcv_multiplier': (1,multiplier)}),
         26: _passive_stats_convert({'for_attr': all_attr, 'atk_multiplier': (0,multiplier)}),
         28: _passive_stats_convert({'for_attr': (0,single_to_list), 'atk_multiplier': (1,multiplier), 'rcv_multiplier': (1,multiplier)}),
         29: _passive_stats_convert({'for_attr': (0,single_to_list), 'hp_multiplier': (1,multiplier), 'atk_multiplier': (1,multiplier), 'rcv_multiplier': (1,multiplier)}),
         30: _passive_stats_convert({'for_type': (slice(0,2),collection_to_list), 'hp_multiplier': (2,multiplier)}),
         31: _passive_stats_convert({'for_type': (slice(0,2),collection_to_list), 'atk_multiplier': (2,multiplier)}),
         33: convert('drumming_sound', {}),
         36: _passive_stats_convert({'reduction_attributes': (slice(0,2),collection_to_list), 'damage_reduction': (2,multiplier)}),
         38: _threshold_stats_convert(_BELOW, {'for_attr': all_attr, 'threshold': (0,multiplier), 'damage_reduction': (2,multiplier)}),
         39: _threshold_stats_convert(_BELOW, {'for_attr': all_attr, 'threshold': (0,multiplier), 'atk_multiplier': (slice(1,4),_atk_from_slice), 'rcv_multiplier': (slice(1,4),_rcv_from_slice)}),
         40: _passive_stats_convert({'for_attr': (slice(0,2),collection_to_list), 'atk_multiplier': (2,multiplier)}),
         41: convert('counter_attack', {'chance': (0,multiplier), 'multiplier': (1,multiplier), 'attribute': (2,cc)}),
         43: _threshold_stats_convert(_ABOVE, {'for_attr': all_attr, 'threshold': (0,multiplier), 'damage_reduction': (2,multiplier)}),
         44: _threshold_stats_convert(_ABOVE, {'for_attr': all_attr, 'threshold': (0,multiplier), 'atk_multiplier': (slice(1,4),_atk_from_slice), 'rcv_multiplier': (slice(1,4),_rcv_from_slice)}),
         45: _passive_stats_convert({'for_attr': (0,single_to_list), 'hp_multiplier': (1,multiplier), 'atk_multiplier': (1,multiplier)}),
         46: _passive_stats_convert({'for_attr': (slice(0,2),collection_to_list), 'hp_multiplier': (2,multiplier)}),
         48: _passive_stats_convert({'for_attr': (0,single_to_list), 'hp_multiplier': (1,multiplier)}),
         49: _passive_stats_convert({'for_attr': (0,single_to_list), 'rcv_multiplier': (1,multiplier)}),
         53: convert('egg_drop_rate', {'multiplier': (0,multiplier)}),
         54: convert('coin_drop_rate', {'multiplier': (0,multiplier)}),
         61: _attribute_match_convert({'attributes': (0,binary_to_list), 'minimum_attributes': (1,cc), 'minimum_atk_multiplier': (2,multiplier), 'minimum_rcv_multiplier': (2,multiplier), 'bonus_atk_multiplier': (3,multiplier), 'bonus_rcv_multiplier': (3,multiplier)}),
         62: _passive_stats_convert({'for_type': (0,single_to_list), 'hp_multiplier': (1,multiplier), 'atk_multiplier': (1,multiplier)}),
         63: _passive_stats_convert({'for_type': (0,single_to_list), 'hp_multiplier': (1,multiplier), 'rcv_multiplier': (1,multiplier)}),
         64: _passive_stats_convert({'for_type': (0,single_to_list), 'atk_multiplier': (1,multiplier), 'rcv_multiplier': (1,multiplier)}),
         65: _passive_stats_convert({'for_type': (0,single_to_list), 'hp_multiplier': (1,multiplier), 'atk_multiplier': (1,multiplier), 'rcv_multiplier': (1,multiplier)}),
         66: _combo_match_convert({'for_attr': all_attr, 'minimum_combos': (0,cc), 'minimum_atk_multiplier': (1,multiplier)}),
         67: _passive_stats_convert({'for_attr': (0,single_to_list), 'hp_multiplier': (1,multiplier), 'rcv_multiplier': (1,multiplier)}),
         69: _passive_stats_convert({'for_attr': (0,single_to_list), 'for_type': (1,single_to_list), 'atk_multiplier': (2,multiplier)}),
         73: _passive_stats_convert({'for_attr': (0,single_to_list), 'for_type': (1,single_to_list), 'hp_multiplier': (2,multiplier), 'atk_multiplier': (2,multiplier)}),
         75: _passive_stats_convert({'for_attr': (0,single_to_list), 'for_type': (1,single_to_list), 'atk_multiplier': (2,multiplier), 'rcv_multiplier': (2,multiplier)}),
         76: _passive_stats_convert({'for_attr': (0,single_to_list), 'for_type': (1,single_to_list), 'hp_multiplier': (2,multiplier), 'atk_multiplier': (2,multiplier), 'rcv_multiplier': (2,multiplier)}),
         77: _passive_stats_convert({'for_type': (slice(0,2),collection_to_list), 'hp_multiplier': (2,multiplier), 'atk_multiplier': (2,multiplier)}),
         79: _passive_stats_convert({'for_type': (slice(0,2),collection_to_list), 'atk_multiplier': (2,multiplier), 'rcv_multiplier': (2,multiplier)}),
         94: _threshold_stats_convert(_BELOW, {'for_attr': (1,single_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (slice(2,5),_atk_from_slice), 'rcv_multiplier': (slice(2,5),_rcv_from_slice)}),
         95: _threshold_stats_convert(_BELOW, {'for_type': (1,single_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (slice(2,5),_atk_from_slice), 'rcv_multiplier': (slice(2,5),_rcv_from_slice)}),
         96: _threshold_stats_convert(_ABOVE, {'for_attr': (1,single_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (slice(2,5),_atk_from_slice), 'rcv_multiplier': (slice(2,5),_rcv_from_slice)}),
         97: _threshold_stats_convert(_ABOVE, {'for_type': (1,single_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (slice(2,5),_atk_from_slice), 'rcv_multiplier': (slice(2,5),_rcv_from_slice)}),
         98: _combo_match_convert({'for_attr': all_attr, 'minimum_combos': (0,cc), 'minimum_atk_multiplier': (1,multiplier), 'bonus_atk_multiplier': (2,multiplier), 'maximum_combos':(3,cc)}),
        100: convert('skill_used_stats', {'for_attr': all_attr, 'for_type': [], 'atk_multiplier': (slice(0,4),_atk_from_slice), 'rcv_multiplier': (slice(0,4),_rcv_from_slice)}),
        101: convert('exact_combo_match', {'combos': (0,cc), 'atk_multiplier': (1,multiplier)}),
        103: _combo_match_convert({'for_attr': all_attr, 'minimum_combos': (0,cc), 'minimum_atk_multiplier': (slice(1,4),_atk_from_slice), 'minimum_rcv_multiplier': (slice(1,4),_rcv_from_slice), 'maximum_combos':(0,cc)}),
        104: _combo_match_convert({'for_attr': (1,binary_to_list), 'minimum_combos': (0,cc), 'minimum_atk_multiplier': (slice(2,5),_atk_from_slice), 'minimum_rcv_multiplier': (slice(2,5),_rcv_from_slice), 'maximum_combos':(0,cc)}),
        105: _passive_stats_convert({'for_attr': all_attr, 'atk_multiplier': (1,multiplier), 'rcv_multiplier': (0,multiplier)}),
        106: _passive_stats_convert({'for_attr': all_attr, 'hp_multiplier': (0,multiplier), 'atk_multiplier': (1,multiplier)}),
        107: _passive_stats_convert({'for_attr': all_attr, 'hp_multiplier': (0,multiplier)}),
        108: convert('passive_stats_type_atk_all_hp', {'for_type': (1,single_to_list), 'atk_multiplier': (2,multiplier), 'hp_multiplier': (0,multiplier)}),
        109: _mass_match_convert({'attributes': (0,binary_to_list), 'minimum_count': (1,cc), 'minimum_atk_multiplier': (2,multiplier)}),
        111: _passive_stats_convert({'for_attr': (slice(0,2),collection_to_list), 'hp_multiplier': (2,multiplier), 'atk_multiplier': (2,multiplier)}),
        114: _passive_stats_convert({'for_attr': (slice(0,2),collection_to_list), 'hp_multiplier': (2,multiplier), 'atk_multiplier': (2,multiplier), 'rcv_multiplier': (2,multiplier)}),
        119: _mass_match_convert({'attributes': (0,binary_to_list), 'minimum_count': (1,cc), 'minimum_atk_multiplier': (2,multiplier), 'bonus_atk_multiplier': (3,multiplier), 'maximum_count': (4,cc)}),
        121: _passive_stats_convert({'for_attr': (0,binary_to_list), 'for_type': (1,binary_to_list), 'hp_multiplier': (2,increase_multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier)}),
        122: _threshold_stats_convert(_BELOW, {'for_attr': (1,binary_to_list), 'for_type': (2,binary_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier)}),
        123: _threshold_stats_convert(_ABOVE, {'for_attr': (1,binary_to_list), 'for_type': (2,binary_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier)}),
        124: _multi_attribute_match_convert({'attributes': (slice(0,5),list_of_binary_to_list), 'minimum_match': (5,cc), 'minimum_atk_multiplier': (6,multiplier), 'bonus_atk_multiplier': (7,multiplier)}),
        125: convert('team_build_bonus', {'monster_ids': (slice(0,5),positive_values_to_list), 'hp_multiplier': (5,increase_multiplier), 'atk_multiplier': (6,increase_multiplier), 'rcv_multiplier': (7,increase_multiplier)}),
        129: _passive_stats_convert({'for_attr': (0,binary_to_list), 'for_type': (1,binary_to_list), 'hp_multiplier': (2,increase_multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier), 'reduction_attributes': (5,binary_to_list), 'damage_reduction': (6,multiplier)}),
        130: _threshold_stats_convert(_BELOW, {'for_attr': (1,binary_to_list), 'for_type': (2,binary_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier), 'reduction_attributes': (5,binary_to_list), 'damage_reduction': (6,multiplier)}),
        131: _threshold_stats_convert(_ABOVE, {'for_attr': (1,binary_to_list), 'for_type': (2,binary_to_list), 'threshold': (0,multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier), 'reduction_attributes': (5,binary_to_list), 'damage_reduction': (6,multiplier)}),
        133: convert('skill_used_stats', {'for_attr': (0,binary_to_list), 'for_type': (1,binary_to_list), 'atk_multiplier': (2,increase_multiplier), 'rcv_multiplier': (3,increase_multiplier)}),
        136: convert('dual_passive_stats', {'for_attr_1': (0,binary_to_list), 'for_type_1': [], 'hp_multiplier_1': (1,increase_multiplier), 'atk_multiplier_1': (2,increase_multiplier), 'rcv_multiplier_1': (3,increase_multiplier), 'for_attr_2': (4,binary_to_list), 'for_type_2': [], 'hp_multiplier_2': (5,increase_multiplier), 'atk_multiplier_2': (6,increase_multiplier), 'rcv_multiplier_2': (7,increase_multiplier)}),
        137: convert('dual_passive_stats', {'for_attr_1': [], 'for_type_1': (0,binary_to_list), 'hp_multiplier_1': (1,increase_multiplier), 'atk_multiplier_1': (2,increase_multiplier), 'rcv_multiplier_1': (3,increase_multiplier), 'for_attr_2': [], 'for_type_2': (4,binary_to_list), 'hp_multiplier_2': (5,increase_multiplier), 'atk_multiplier_2': (6,increase_multiplier), 'rcv_multiplier_2': (7,increase_multiplier)}),
        138: convert('combine_leader_skills', {'skill_ids': (slice(None),collection_to_list)}),
        139: convert('dual_threshold_stats', {'for_attr': (0,binary_to_list), 'for_type': (1,binary_to_list),
            'threshold_1': (2,multiplier), 'above_1': (3,lambda x: not bool(x)), 'atk_multiplier_1': (4,multiplier), 'rcv_multiplier_1': 1.0, 'damage_reduction_1': 0.0,
            'threshold_2': (5,multiplier), 'above_2': (6,lambda x: not bool(x)), 'atk_multiplier_2': (7,multiplier), 'rcv_multiplier_2': 1.0, 'damage_reduction_2': 0.0}),
        148: convert('rank_experience_rate', {'multiplier': (0,multiplier)}),
        149: convert('heath_tpa_stats', {'rcv_multiplier': (0,multiplier)}),
        150: convert('five_orb_one_enhance', {'atk_multiplier': (1,multiplier)}),
        151: convert('heart_cross', {'atk_multiplier': (0,increase_multiplier), 'rcv_multiplier': (1,increase_multiplier), 'damage_reduction': (2,multiplier)}),
        155: convert('multiplayer_stats', {'for_attr': (0,binary_to_list), 'for_type': (1,binary_to_list), 'hp_multiplier': (2,increase_multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier)}),
        157: convert('color_cross', {'crosses': (slice(None), lambda x: [{'attribute':a,'atk_multiplier':multiplier(d)} for a,d in zip(x[::2],x[1::2])])}),
        158: convert('minimum_match', {'minimum_match': (0,cc), 'for_attr': (1,binary_to_list), 'for_type': (2,binary_to_list), 'hp_multiplier': (4,increase_multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (5,increase_multiplier)}),
        159: _mass_match_convert({'attributes': (0,binary_to_list), 'minimum_count': (1,cc), 'minimum_atk_multiplier': (2,multiplier), 'bonus_atk_multiplier': (3,multiplier), 'maximum_count': (4,cc)}),
        162: convert('large_board', {'for_attr': [], 'for_type': [], 'hp_multiplier': 1.0, 'atk_multiplier': 1.0, 'rcv_multiplier': 1.0}),
        163: convert('no_skyfall', {}),
        164: _multi_attribute_match_convert({'attributes': (slice(0,4),list_of_binary_to_list), 'minimum_match': (4,cc), 'minimum_atk_multiplier': (5,multiplier), 'minimum_rcv_multiplier': (6,multiplier), 'bonus_atk_multiplier': (7,multiplier), 'bonus_rcv_multiplier': (7,multiplier)}),
        165: _attribute_match_convert({'attributes': (0,binary_to_list), 'minimum_attributes': (1,cc), 'minimum_atk_multiplier': (2,multiplier), 'minimum_rcv_multiplier': (3,multiplier), 'bonus_atk_multiplier': (4,multiplier), 'bonus_rcv_multiplier': (5,multiplier), 'maximum_attributes': (slice(1,7,6),lambda x: x[0] + x[1])}),
        166: _combo_match_convert({'for_attr': all_attr, 'minimum_combos': (0,cc), 'minimum_atk_multiplier': (1,multiplier), 'minimum_rcv_multiplier': (2,multiplier), 'bonus_atk_multiplier': (3,multiplier), 'bonus_rcv_multiplier': (4,multiplier), 'maximum_combos':(5,cc)}),
        167: _mass_match_convert({'attributes': (0,binary_to_list), 'minimum_count': (1,cc), 'minimum_atk_multiplier': (2,multiplier), 'minimum_rcv_multiplier': (3,multiplier), 'bonus_atk_multiplier': (4,multiplier), 'bonus_rcv_multiplier': (5,multiplier), 'maximum_count': (6,cc)}),
        169: _combo_match_convert({'for_attr': all_attr, 'minimum_combos': (0,cc), 'minimum_atk_multiplier': (1,multiplier), 'minimum_damage_reduction': (2,multiplier)}),
        170: _attribute_match_convert({'attributes': (0,binary_to_list), 'minimum_attributes': (1,cc), 'minimum_atk_multiplier': (2,multiplier), 'minimum_damage_reduction': (3,multiplier)}),
        171: _multi_attribute_match_convert({'attributes': (slice(0,4),list_of_binary_to_list), 'minimum_match': (4,cc), 'minimum_atk_multiplier': (5,multiplier), 'minimum_damage_reduction': (6,multiplier)}),
        175: convert('collab_bonus', {'collab_id': (0,cc), 'hp_multiplier': (3,increase_multiplier), 'atk_multiplier': (4,increase_multiplier), 'rcv_multiplier': (5,increase_multiplier)}),
        177: convert('orbs_remaining', {'orb_count': (5,cc), 'atk_multiplier': (6,multiplier)}),
        178: convert('fixed_move_time', {'time': (0,cc), 'for_attr': (1,binary_to_list), 'for_type': (2,binary_to_list), 'hp_multiplier': (3,increase_multiplier), 'atk_multiplier': (4,increase_multiplier), 'rcv_multiplier': (5,increase_multiplier)}),
        182: _mass_match_convert({'attributes': (0,binary_to_list), 'minimum_count': (1,cc), 'minimum_atk_multiplier': (2,multiplier), 'minimum_damage_reduction': (3,multiplier)}),
        183: convert('dual_threshold_stats', {'for_attr': (0,binary_to_list), 'for_type': (1,binary_to_list),
            'threshold_1': (2,multiplier), 'above_1': True, 'atk_multiplier_1': (3,multiplier), 'rcv_multiplier_1': 1.0, 'damage_reduction_1': (4,multiplier),
            'threshold_2': (5,multiplier), 'above_2': False, 'atk_multiplier_2': (6,increase_multiplier), 'rcv_multiplier_2': (7,increase_multiplier), 'damage_reduction_2': 0.0}),
        185: convert('bonus_move_time', {'time': (0,multiplier), 'for_attr': (1,binary_to_list), 'for_type': (2,binary_to_list), 'hp_multiplier': (3,increase_multiplier), 'atk_multiplier': (4,increase_multiplier), 'rcv_multiplier': (5,increase_multiplier)}),
        186: convert('large_board', {'for_attr': (0,binary_to_list), 'for_type': (1,binary_to_list), 'hp_multiplier': (2,increase_multiplier), 'atk_multiplier': (3,increase_multiplier), 'rcv_multiplier': (4,increase_multiplier)}),
    }

    def parsable(self, raw_data: dict) -> bool:
        return 'skill' in raw_data

    def version(self) -> int:
        return 1220

    def parse(self, raw_data: dict) -> dict:
        self._clear_reports()
        
        parsed_json = {}
        parsed_json['version'] = raw_data['v']
        parsed_json['active_skills'] = {}
        parsed_json['leader_skills'] = {}
        
        for i,skill_data in enumerate(raw_data['skill']):
            if skill_data[3] == 0 and skill_data[4] == 0: # this distinguishes leader skills from active skills
                parsed_json['leader_skills'][i] = {}
                parsed_json['leader_skills'][i]['id'] = i
                parsed_json['leader_skills'][i]['name'] = skill_data[0]
                parsed_json['leader_skills'][i]['card_description'] = skill_data[1]
                if skill_data[2] in SkillParser._skills:
                    parsed_json['leader_skills'][i]['type'],parsed_json['leader_skills'][i]['args'] = SkillParser._skills[skill_data[2]](skill_data[6:])
                else:
                    self._report(f'Found unexpected leader skill ( id: {i}, type:{skill_data[2]} )')
                    parsed_json['leader_skills'][i]['type'] = 'unexpected'
                    parsed_json['leader_skills'][i]['args'] = {'type': skill_data[2]}
            else:
                parsed_json['active_skills'][i] = {}
                parsed_json['active_skills'][i]['id'] = i
                parsed_json['active_skills'][i]['name'] = skill_data[0]
                parsed_json['active_skills'][i]['card_description'] = skill_data[1]
                parsed_json['active_skills'][i]['max_skill'] = skill_data[3]
                parsed_json['active_skills'][i]['base_cooldown'] = skill_data[4]
                if skill_data[2] in SkillParser._skills:
                    parsed_json['active_skills'][i]['type'],parsed_json['active_skills'][i]['args'] = SkillParser._skills[skill_data[2]](skill_data[6:])
                else:
                    self._report(f'Found unexpected active skill ( id: {i}, type:{skill_data[2]} )')
                    parsed_json['active_skills'][i]['type'] = 'unexpected'
                    parsed_json['active_skills'][i]['args'] = {'type': skill_data[2]}

        def verify(skills):
            type_verification = defaultdict(lambda: defaultdict(set))
            for skill in skills.values():
                type_verification[skill['type']]['_arg_names'].add(frozenset(skill['args'].keys()))
                for arg_name,arg_value in skill['args'].items():
                    type_verification[skill['type']][arg_name].add(type(arg_value))
            for skill_type,args in type_verification.items():
                for arg_name,arg_types in args.items():
                    if len(arg_types) != 1:
                        self._report_dev(f'Inconsistent type: {skill_type} difference in {repr(arg_name)}: {repr(arg_types)}')

        verify(parsed_json['active_skills'])
        verify(parsed_json['leader_skills'])

        return parsed_json
