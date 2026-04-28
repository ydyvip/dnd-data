# -*- coding: utf-8 -*-
"""
《暗影王座的救赎》游戏配置
所有游戏常量集中管理，便于调整平衡性
"""

# ============================================================
# 游戏基础设置
# ============================================================
MAX_LEVEL = 20
STARTING_GOLD = 100
STARTING_HEALTH = 100
EXPERIENCE_PER_LEVEL = 1000
HEALTH_PER_LEVEL = 10
STAT_INCREASE_PER_LEVEL = 2

# ============================================================
# 角色创建默认属性
# ============================================================
DEFAULT_ATTRIBUTE = 10
CLASS_STAT_PRIMARY = 16
CLASS_STAT_SECONDARY = 14

# ============================================================
# 道德系统配置 (文档要求 -10 ~ +10)
# ============================================================
MORALITY_MIN = -10
MORALITY_MAX = 10

# 道德值对法术的修正
MORALITY_SPELL_BONUS_THRESHOLD = 6   # 道德值 ≥6 时获得法术加成
MORALITY_LIGHT_SPELL_BONUS = 2       # 光明高 → 神圣/光明法术 +2
MORALITY_SHADOW_SPELL_BONUS = 2      # 暗影高 → 暗影法术 +2
MORALITY_BALANCE_SPELL_BONUS = 1     # 平衡高 → 所有法术 +1

# 道德解锁对话选项阈值
MORALITY_DIALOGUE_GOOD_THRESHOLD = 5   # 光明 ≥5 解锁善良对话
MORALITY_DIALOGUE_EVIL_THRESHOLD = 5   # 暗影 ≥5 解锁邪恶对话
MORALITY_DIALOGUE_NEUTRAL_THRESHOLD = 5  # 平衡 ≥5 解锁理性对话

# ============================================================
# 结局触发条件 (匹配结局判定系统.md)
# ============================================================
# 光明结局
ENDING_LIGHT_LIGHT_MIN = 12
ENDING_LIGHT_SHADOW_MAX = 3
ENDING_LIGHT_BALANCE_MIN = 0
ENDING_LIGHT_NPC_RELATIONSHIP_MIN = 6
ENDING_LIGHT_NPC_HIGH_RELATIONSHIP_COUNT = 3
ENDING_LIGHT_NPC_HIGH_RELATIONSHIP_MIN = 8

# 黑暗结局
ENDING_SHADOW_SHADOW_MIN = 12
ENDING_SHADOW_LIGHT_MAX = 3
ENDING_SHADOW_BALANCE_MAX = -2

# 平衡结局
ENDING_BALANCE_LIGHT_MIN = 4
ENDING_BALANCE_LIGHT_MAX = 7
ENDING_BALANCE_SHADOW_MIN = 4
ENDING_BALANCE_SHADOW_MAX = 7

# ============================================================
# 环境战斗系统
# ============================================================
TERRAIN_MODIFIERS = {
    "平原":   {"attack": 0, "defense": 0, "move": 0, "ranged": 0, "description": "无特殊效果"},
    "高地":   {"attack": 0, "defense": 0, "move": 0, "ranged": 2, "description": "远程攻击+2"},
    "森林":   {"attack": -1, "defense": 2, "move": -5, "ranged": -2, "description": "AC+2，移动-5尺，远程劣势"},
    "室内":   {"attack": 0, "defense": 2, "move": -5, "ranged": -2, "description": "AC+2，空间受限"},
    "水域":   {"attack": -2, "defense": -2, "move": -10, "ranged": -2, "description": "速度减半，火系+2"},
    "狭窄通道": {"attack": 0, "defense": 1, "move": -10, "ranged": -2, "description": "近战优势通道"}
}

WEATHER_MODIFIERS = {
    "晴天": {"fire": 0, "water": 0, "cold": 0, "ranged": 0, "move": 0, "description": "所有法术正常"},
    "雨天": {"fire": -2, "water": 2, "cold": 0, "ranged": -2, "move": 0, "description": "火系-2，水系+2，远程劣势"},
    "雪天": {"fire": 0, "water": 0, "cold": 2, "ranged": 0, "move": -5, "description": "寒冷+2，移动-5尺"},
    "雾天": {"fire": 0, "water": 0, "cold": 0, "ranged": -4, "move": 0, "description": "视野减半，远程劣势"},
}

# ============================================================
# 团队组合技
# ============================================================
TEAM_COMBOS = {
    "双重打击": {
        "description": "两个相邻角色同时攻击同一目标，第二个攻击获得优势，伤害+1",
        "min_players": 2,
        "damage_bonus": 1,
        "attack_advantage": True
    },
    "掩护射击": {
        "description": "一个角色提供掩护，另一个攻击，攻击者AC+2",
        "min_players": 2,
        "defense_bonus": 2,
        "requires_bonus_action": True
    },
    "夹击战术": {
        "description": "两个角色从不同方向攻击，目标劣势，伤害+2",
        "min_players": 2,
        "damage_bonus": 2,
        "target_disadvantage": True
    },
    "集体护盾": {
        "description": "相邻角色共享护盾，集体AC+1，可分担伤害",
        "min_players": 2,
        "defense_bonus": 1,
        "damage_sharing": True
    },
    "元素共鸣": {
        "description": "两个相同元素法术叠加，效果+2，范围+50%",
        "min_players": 2,
        "spell_bonus": 2,
        "range_multiplier": 1.5
    }
}

# ============================================================
# 装备套装效果 (战斗规则补充.md)
# ============================================================
EQUIPMENT_SETS = {
    "光明套装": {
        "pieces": 4,
        "bonuses": {
            2: {"healing_bonus": 1, "description": "治疗法术效果+1"},
            3: {"advantage_against_shadow": True, "description": "对抗暗影生物获得优势"},
            4: {"divine_protection": True, "description": "每天一次神圣庇护（免疫一次恐惧）"}
        }
    },
    "暗影套装": {
        "pieces": 4,
        "bonuses": {
            2: {"darkvision_enhanced": True, "description": "暗影视野增强"},
            3: {"shadow_invisibility": True, "description": "暗影中获得隐身"},
            4: {"shadow_link": True, "description": "暗影链接（与队友共享暗影力量）"}
        }
    },
    "平衡套装": {
        "pieces": 4,
        "bonuses": {
            2: {"all_stats_plus_1": True, "description": "所有属性+1"},
            3: {"element_resistance_plus_1": True, "description": "元素抗性+1"},
            4: {"balance_guardian": True, "description": "平衡守护（每天一次）"}
        }
    }
}

# ============================================================
# 法术协同配置 (战斗规则补充.md)
# ============================================================
SPELL_SYNERGIES = {
    ("火焰", "冷冻"): {"name": "蒸汽云", "effect": "提供掩护但降低视野", "defense_bonus": 2, "ranged_penalty": -2},
    ("火焰", "风暴"): {"name": "火焰旋风", "effect": "造成持续伤害", "dot_damage": "1d6"},
    ("冷冻", "风暴"): {"name": "暴风雨", "effect": "降低远程攻击效果", "ranged_penalty": -4},
    ("大地", "冷冻"): {"name": "泥潭", "effect": "降低移动速度", "move_penalty": -15},
    ("光明", "暗影"): {"name": "能量爆发", "effect": "造成大量伤害", "damage_bonus": 4}
}

# ============================================================
# BOSS阶段配置
# ============================================================
BOSS_PHASE_TEMPLATES = {
    "phase1": {
        "name": "标准形态",
        "hp_multiplier": 1.0,
        "attack_multiplier": 1.0,
        "defense_multiplier": 1.0,
        "abilities": ["基础AOE攻击"]
    },
    "phase2": {
        "name": "能量形态",
        "hp_multiplier": 0.7,
        "attack_multiplier": 1.3,
        "defense_multiplier": 1.2,
        "abilities": ["范围伤害", "强力控制"]
    },
    "phase3": {
        "name": "真身形态",
        "hp_multiplier": 0.5,
        "attack_multiplier": 1.5,
        "defense_multiplier": 1.3,
        "abilities": ["终极技能", "全场效果"]
    }
}

# ============================================================
# 存档配置
# ============================================================
SAVE_DIR = "saves"
SAVE_FILE_EXTENSION = ".json"
MAX_SAVE_SLOTS = 9
