from .json_parser import JsonParser
from .common import *
from collections import defaultdict

def _orb_convert(from_index, args):
    def internal(x):
        if defaultlist(int,x)[from_index] < 0:
            return convert('orb_convert_random', {'from_count': (args['from'][0], lambda x: abs(args['from'][1](x))), 'to': args['to'], 'damage': args['damage']})(x)
        return convert('orb_convert', {'from': args['from'], 'to': args['to'], 'damage': args['damage']})(x)
    return internal

_orb_spawn_defaults = {'damage': 0.0, 'amount': 0, 'orbs': [], 'exclude_orbs': []}
def _orb_spawn(arguments):
    return convert('spawn_orbs', {k:(arguments[k] if k in arguments else v) for k,v in _orb_spawn_defaults.items()})
    
_all_slots = [0,1,2,3,4,5]
def _card_bind_slots(b):
    if b == 0:
        return _all_slots
    result = []
    if b & 1:
        result.append(0)
    if b >> 2 & 1:
        result.extend([1,2,3,4])
    if b >> 1 & 1:
        result.append(5)
    return result

def _card_bind(arguments):
    arguments['damage'] = arguments['damage'] if 'damage' in arguments else 0.0
    arguments['slots'] = arguments['slots'] if 'slots' in arguments else []
    arguments['types'] = arguments['types'] if 'types' in arguments else []
    arguments['attributes'] = arguments['attributes'] if 'attributes' in arguments else []
    arguments['card_count'] = arguments['card_count'] if 'card_count' in arguments else 6
    return convert('card_bind', arguments)

def _pattern(values):
    result = []
    for value in values:
        r = []
        for c in range(6):
            r.append(value >> c & 1)
        result.append(r)
    return result

_pos_x = {0: 0, 1: 1, 2: 2, 3: 3, 4: -3, 5: -2, 6: -1}
def _position_x(x):
    if x in _pos_x:
        return _pos_x[x]
    raise ValueError(f'Invalid x position: {x}')

_pos_y = {1: 0, 2: 1, 3: 2, 3: 3, 4: -2, 5: -1}
def _position_y(y):
    if y in _pos_y:
        return _pos_y[y]
    raise ValueError(f'Invalid y position: {y}')


class EnemySkillParser(JsonParser):
    _enemy_skills = {
        0:   convert('null_skill', {}),
        1:   _card_bind({'slots': _all_slots, 'card_count': (0,lambda x: max(1,x)), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc)}),
        2:   _card_bind({'attributes': (0,single_to_list), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc)}),
        3:   _card_bind({'types': (0,single_to_list), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc)}),
        4:   _orb_convert(0, {'damage': 0.0, 'from': (0,cc), 'to': (1,cc)}),
        5:   convert('normal_blind', {'damage': 0.0}),
        6:   convert('dispel', {}),
        7:   convert('enemy_heal', {'minimum_percentage': (0,multiplier), 'maximum_percentage': (1,multiplier)}),
        8:   convert('next_attack_boost', {'minimum_percentage': (0,increase_multiplier), 'maximum_percentage': (1,increase_multiplier)}),
        9:   unimplimented(9),
        10:  unimplimented(10),
        11:  unimplimented(11),
        12:  _orb_convert(0, {'damage': 0.0, 'from': (0,cc), 'to': 6}),
        13:  _orb_convert(0, {'damage': 0.0, 'from': (0,lambda x: -x), 'to': 6}),
        14:  convert('skill_bind', {'minimum_duration': (0,cc), 'maximum_duration': (1,cc)}),
        15:  convert('multi_attack', {'minimum_hits': (0,cc), 'maximum_hits': (1,cc), 'damage': (2,multiplier)}),
        16:  convert('skip', {}), # does nothing but say text
        17:  convert('attack_boost_1', {'un': (0,cc), 'duration': (1,cc), 'multiplier': (2,multiplier)}), ### look into this later
        18:  convert('attack_boost_2', {'duration': (0,cc), 'multiplier': (1,multiplier)}), ### look into this later
        19:  convert('attack_boost_3', {'un': (0,cc), 'duration': (1,cc), 'multiplier': (2,multiplier)}), ### look into this later
        20:  convert('status_shield', {'duration': (2,cc)}),
        21:  convert('_unused_1', {}), # unused  #the following are special skills used to control monster behavior, details later
        22:  convert('_flag_set', {}), # Set flag {ai} to True
        23:  convert('_if_flag_jump_0_index', {}), # If flag {ai} is True, jump to action {rnd+1}?
        24:  convert('_flag_remove', {}), # Set flag {ai} to False
        25:  convert('_counter_set', {}), # Set counter to {ai}
        26:  convert('_counter_add', {}), # Add 1 to counter
        27:  convert('_counter_subtract', {}), # Subtract 1 from counter
        28:  convert('_if_hp_below_jump', {}), # If HP is less than (or equal to?) {ai}%, jump to action {rnd}
        29:  convert('_if_hp_above_jump', {}), # If HP is more than (or equal to?) {ai}%, jump to action {rnd}
        30:  convert('_if_counter_below_jump', {}), # If counter is less than (or equal to?) {ai}, jump to action {rnd}
        31:  convert('_if_counter_equal_jump', {}), # If counter is equal to {ai}, jump to action {rnd}
        32:  convert('_if_counter_above_jump', {}), # If counter is more than (or equal to?) {ai}, jump to action {rnd}
        33:  convert('_if_level_below_jump', {}), # If counter is less than (or equal to?) {ai}, jump to action {rnd}
        34:  convert('_if_level_equal_jump', {}), # If counter is equal to {ai}, jump to action {rnd}
        35:  convert('_if_level_below_jump', {}),
        36:  convert('_end_path', {}), # seems to force a normal attack, but most recent monsters use them as unreachable buffers
        37:  convert('_display_counter', {}), # unused?
        38:  convert('_if_counter_set', {}), # unsure of exact meaning, guess: Set (flag?) {rnd} when counter equals {ai}?
        39:  convert('time_debuff', {'duration': (0,cc), 'static': (1,lambda x: x/10), 'percentage': (2,multiplier)}),
        40:  convert('suicide', {}),
        41:  unimplimented(41),
        42:  unimplimented(42),
        43:  convert('_if_flag_jump', {}), # If flag {ai} is True, jump to action {rnd}?
        44:  convert('_or_flag', {}), # MUST LOOK INTO
        45:  convert('_xor_flag', {}), # MUST LOOK INTO
        46:  convert('element_change', {'attribute_pool': (slice(0,5), lambda x: list(set(x)))}),
        47:  convert('normal_attack', {'damage': (0,multiplier)}),
        48:  _orb_convert(1, {'damage': (0,multiplier), 'from': (1,cc), 'to': (2,cc)}),
        49:  convert('_preemptive', {'minimum_level': (0,cc)}),
        50:  convert('gravity', {'amount': (0,multiplier)}),
        51:  unimplimented(51),
        52:  convert('revive', {'percentage_hp': (0,multiplier)}),
        53:  convert('absorb_attribute', {'minimum_duration': (0,cc), 'maximum_duration': (1,cc), 'attributes': (2,binary_to_list)}),
        54:  _card_bind({'slots': (0,_card_bind_slots), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc)}),
        55:  convert('player_heal', {'minimum_amount': (0,multiplier), 'maximum_amount': (1,multiplier)}),
        56:  _orb_convert(0, {'damage': 0.0, 'from': (0,cc), 'to': 7}),
        57:  unimplimented(57),
        58:  unimplimented(58),
        59:  unimplimented(59),
        60:  _orb_spawn({'amount': (0,cc), 'orbs': [7], 'exclude_orbs': [7]}),
        61:  _orb_spawn({'amount': (0,cc), 'orbs': [8], 'exclude_orbs': [8]}),
        62:  convert('normal_blind', {'damage': (0,multiplier)}),
        63:  _card_bind({'damage': (0,multiplier), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc), 'slots': (3,_card_bind_slots), 'card_count': (4,lambda x: max(1,x))}),
        64:  _orb_spawn({'damage': (0,multiplier), 'amount': (1,cc), 'orbs': [7], 'exclude_orbs': [7]}),
        65:  _card_bind({'slots': [1,2,3,4], 'card_count': (0,cc), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc)}),
        66:  convert('skip', {}),
        67:  convert('absorb_combo', {'minimum_duration': (0,cc), 'maximum_duration': (1,cc), 'combo_count': (2,cc)}),
        68:  convert('change_skyfall', {'orbs': (0,binary_to_list), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc), 'percentage': (3,multiplier)}),
        69:  convert('transformation', {}), # first skill, passive, animation for transformation on death, eg. nordis
        70:  unimplimented(70),
        71:  convert('void_damage', {'duration': (0,cc), 'amount': (2,cc)}), # unused? flag for what to void
        72:  convert('passive_attribute_reduction', {'attributes': (0,binary_to_list), 'reduction': (1,multiplier)}),
        73:  convert('passive_resolve', {'threshold': (0,multiplier)}),
        74:  convert('damage_shield', {'duration': (0,cc), 'reduction': (1,multiplier)}),
        75:  convert('leader_swap', {'duration': (0,cc)}),
        76:  convert('column_change', {'damage': 0.0, 'columns': (slice(None),lambda x: [{'index':i if i < 3 else i-6,'orbs':binary_to_list(orbs)} for indices,orbs in zip(x[::2],x[1::2]) for i in binary_to_list(indices)])}), # order 0 1 2 -3 -2 -1
        77:  convert('column_change', {'damage': (6,multiplier), 'columns': (slice(0,6),lambda x: [{'index':i if i < 3 else i-6,'orbs':binary_to_list(orbs)} for indices,orbs in zip(x[::2],x[1::2]) for i in binary_to_list(indices)])}),
        78:  convert('row_change', {'damage': 0.0, 'rows': (slice(None),lambda x: [{'index':i if i < 2 else i-5,'orbs':binary_to_list(orbs)} for indices,orbs in zip(x[::2],x[1::2]) for i in binary_to_list(indices)])}),       # order 0 1 -3 -2 -1
        79:  convert('row_change', {'damage': (6,multiplier), 'rows': (slice(0,6),lambda x: [{'index':i if i < 2 else i-5,'orbs':binary_to_list(orbs)} for indices,orbs in zip(x[::2],x[1::2]) for i in binary_to_list(indices)])}),
        80:  unimplimented(80),
        81:  convert('board_change', {'damage': (0,multiplier), 'attributes': (slice(1,None),lambda x: [v for v in x if v != -1])}),
        82:  convert('normal_attack', {'damage': 1.0}), # unsure of extra, seems like a normal 100% damage hit
        83:  convert('combine_enemy_skills', {'skill_ids': (slice(None),collection_to_list)}),
        84:  convert('board_change', {'damage': 0.0, 'attributes': (0,binary_to_list)}),
        85:  convert('board_change', {'damage': (0,multiplier), 'attributes': (1,binary_to_list)}),
        86:  convert('enemy_heal', {'minimum_percentage': (0,multiplier), 'maximum_percentage': (1,multiplier)}),
        87:  convert('absorb_damage', {'duration': (0,cc), 'amount': (1,cc)}),
        88:  convert('awoken_bind', {'duration': (0,cc)}),
        89:  convert('skill_delay', {'minimum_amount': (0,cc), 'maximum_amount': (0,cc)}),
        90:  convert('_if_on_team_jump', {'monster_ids': (slice(None), lambda x: [i for i in x if i != 0])}), # if one of the cards in monster_ids is on the team, jump to {rnd}
        91:  unimplimented(91),
        92:  _orb_spawn({'amount': (0,cc), 'orbs': (1,binary_to_list), 'exclude_orbs': (2,binary_to_list)}),
        93:  unimplimented(93), # Unsure how to handle properly, found only on the original final fantasy dungeon boss, something to do with special effects
        94:  convert('lock_orbs', {'amount': (1,cc), 'attributes': (0,binary_to_list)}),
        95:  convert('passive_on_death', {'skill_id': (0,cc)}), # On death ability, registered through a passive (see anji for example)
        96:  convert('lock_skyfall', {'specific_attributes': (0,lambda x: binary_to_list(x) if x != -1 else []), 'minimum_duration': (1,cc), 'maximum_duration': (2,cc), 'chance': (3,multiplier)}), # specific_attributes is the attributes locked, or empty list for all
        97:  convert('super_blind', {'duration': (0,cc), 'minimum_amount': (1,cc), 'maximum_amount': (2,cc)}), # random orbs
        98:  convert('super_blind_pattern', {'duration': (0,cc), 'pattern': (slice(1,6),_pattern)}), # list of rows; 7x6 boards copy row 3 (1-index from top) to rows 3 and 4, and column 4 (1-index from left) to columns 4 and 5
        99:  convert('scroll_lock', {'duration': (1,cc), 'rows': [], 'columns': (0,lambda x: [i if i < 4 else i-6 for i in binary_to_list(x)])}), # scroll attacks like khepri and azazel
        100: convert('scroll_lock', {'duration': (1,cc), 'columns': [], 'rows': (0,lambda x: [i if i < 3 else i-5 for i in binary_to_list(x)])}),
        101: lambda x: \
        convert('fixed_start', {})(x) \
        if defaultlist(int,x)[0] == 1 else \
        convert('fixed_start_position', {'positon_x': (1,_position_x), 'position_y': (2,_position_y)})(x), # subject to change, I don't understand the positions yet. 3 cases: Phoenix Wright 4,1->3rd from right,top; Lakshmi 6,1->right,top (7x6 too); Leeza 0,5->left,bottom (7x6 too)
        102: _orb_spawn({'damage': 0.0, 'amount': (1,cc), 'orbs': [9], 'exclude_orbs': [9]}), #unsure of bomb index, since it is never stated in game files (but it would be in the source code)
        103: convert('bomb_pattern', {'pattern': (slice(1,6),_pattern), 'locked': (7,bool)}),
        104: lambda x: \
        convert('cloud_spawn', {'duration': (0,cc), 'width': (1,cc), 'height': (2,cc)})(x) \
        if defaultlist(int,x)[3:5] == [0,0] else \
        convert('cloud_spawn_position', {'duration': (0,cc), 'width': (1,cc), 'height': (2,cc), 'positon_x': (3,cc), 'position_y': (4,cc)})(x),
        # unsure of full behavior with 7x6, I think it acts like a pattern, duplicating column 4 and row 3, even after placement
        105: convert('rcv_debuff', {'duration': (0,cc), 'multiplier': (1,multiplier)}), # not always debuff, eg 2x rcv
        106: convert('passive_next_turn_change_threshold', {'threshold': (0,multiplier), 'turn': (1,cc)}), # change turn timer when hp reduced to xx%, then immediately take a turn
        107: convert('unmatchable', {'duration': (0,cc), 'attributes': (1,binary_to_list)}), #eg. Enoch
        108: convert('orb_convert_multiple', {'damage': (0,multiplier), 'from_attributes': (1,binary_to_list), 'to_attributes': (2,binary_to_list)}), #unsure if to_attributes forces 3 of each
        109: convert('spinner_random', {'duration': (0,cc), 'speed': (1,multiplier), 'amount': (2,cc)}),
        110: convert('spinner_pattern', {'duration': (0,cc), 'speed': (1,multiplier), 'pattern': (slice(2,7),_pattern)}),
        111: unimplimented(111),
        112: convert('force_attack', {'duration': (0,cc)}), #eg. hexazeon shield
        113: convert('_if_combo_above_jump', {}), # if the player reached {ai} or more combos last turn, jump to action {rnd}
        114: unimplimented(114),
        115: unimplimented(115),
        116: unimplimented(116),
        117: unimplimented(117),
        118: convert('passive_type_reduction', {'types': (0,binary_to_list), 'reduction': (1,multiplier)}),
        119: convert('null_damage_shield', {}), # satan void turn 1, gilles legato
        120: convert('_if_enemy_remain_equals_jump', {}), # if {ai} enemies remain, jump to action {rnd}
        121: convert('remove_null_damage_shield', {}), # applies to shields from both 119 and 123
        122: convert('passive_next_turn_change_enemies', {'enemy_count': (0,cc), 'turn': (1,cc)}), # change turn timer when xx or less enemies remain, then immediately take a turn. eg. hexa, hexa yellow jewel, gilles legato
        123: convert('null_damage_shield', {}), # hexa only, unsure if meaning is different
    }

    def parsable(self, raw_data: dict) -> bool:
        return 'enemy_skills' in raw_data

    def version(self) -> int:
        return 2

    def parse(self, raw_data: dict) -> dict:
        self._clear_reports()

        parsed_json = {}
        parsed_json['version'] = raw_data['v']
        parsed_json['enemy_skills'] = {}

        raw_csv = gungho_csv(raw_data['enemy_skills'])
        for raw_skill in raw_csv:
            if raw_skill[0] != 'c': # ckey
                parsed_skill = {}
                parsed_skill['id'] = int(raw_skill[0])
                if len(raw_skill[1]) > 1 and raw_skill[1][0] == raw_skill[1][-1] == "'":
                    parsed_skill['text'] = raw_skill[1][1:-1]
                else:
                    parsed_skill['text'] = raw_skill[1]
                parsed_skill['type'] = int(raw_skill[2])
                skill_arg_names = ['text_after', 'param_0', 'param_1', 'param_2', 'param_3',
                                                'param_4', 'param_5', 'param_6', 'param_7',
                                'ratio', 'ai_param_0', 'ai_param_1', 'ai_param_2', 'ai_param_3', 'ai_param_4']
                skill_arg_defaults = ['', 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 10000, 0, 0]
                raw_skill_args_defined = hex_to_list(raw_skill[3])
                def arg_convert(arg):
                    if type(arg) != int and len(arg) > 1 and arg[0] == arg[-1] == "'":
                        return arg[1:-1]
                    else:
                        try:
                            return int(arg)
                        except:
                            return arg

                skill_args = {skill_arg_names[i]:(arg_convert(raw_skill[4 + raw_skill_args_defined.index(i)]) if i in raw_skill_args_defined else skill_arg_defaults[i]) for i in range(15)}
                parsed_skill['text_after'] = skill_args['text_after']
                parsed_skill['ratio'] = skill_args['ratio']
                parsed_skill['ai_param_0'] = int(skill_args['ai_param_0'])
                parsed_skill['hp_threshold'] = int(skill_args['ai_param_1'])/100 # if hp % >= hp_threshold % then ...
                parsed_skill['ai_param_2'] = int(skill_args['ai_param_2'])
                parsed_skill['ai_param_3'] = int(skill_args['ai_param_3'])
                parsed_skill['damage'] = int(skill_args['ai_param_4'])/100 # eventually check for damage in args and place here

                parameter_list = [skill_args['param_'+str(i)] for i in range(8)]
                if int(raw_skill[2]) in EnemySkillParser._enemy_skills:
                    parsed_skill['type'],parsed_skill['args'] = EnemySkillParser._enemy_skills[int(raw_skill[2])](parameter_list)
                else:
                    self._report(f'Found unexpected enemy skill ( id: {raw_skill[0]}, type:{raw_skill[2]} )')
                    parsed_skill['type'] = 'unexpected'
                    parsed_skill['args'] = {'type': raw_skill[2]}

                parsed_json['enemy_skills'][parsed_skill['id']] = parsed_skill
        
        def verify(skills):
            type_verification = defaultdict(lambda: defaultdict(set))
            for i,skill in skills.items():
                type_verification[skill['type']]['_arg_names'].add(frozenset(skill['args'].keys()))
                for arg_name,arg_value in skill['args'].items():
                    type_verification[skill['type']][arg_name].add(type(arg_value))
            for skill_type,args in type_verification.items():
                for arg_name,arg_types in args.items():
                    if len(arg_types) != 1:
                        self._report_dev(f'Inconsistent type: {skill_type} difference in {repr(arg_name)}: {repr(arg_types)}')

        verify(parsed_json['enemy_skills'])

        return parsed_json
