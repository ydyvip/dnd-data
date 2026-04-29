"""
《暗影王座的救赎》数据模型层
包含所有纯数据结构（dataclass），与业务逻辑解耦
"""

import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional


# ---------------------------------------------------------------------------
# 枚举类型
# ---------------------------------------------------------------------------

class ValueType(Enum):
    """角色属性类型"""
    STRENGTH = "力量"
    DEXTERITY = "敏捷"
    CONSTITUTION = "体质"
    INTELLIGENCE = "智力"
    WISDOM = "感知"
    CHARISMA = "魅力"


class MoralityType(Enum):
    """道德类型"""
    LIGHT = "光明"
    SHADOW = "暗影"
    BALANCE = "平衡"


class SkillType(Enum):
    """技能类型"""
    COMBAT = "战斗"
    MAGIC = "魔法"
    STEALTH = "潜行"
    SOCIAL = "社交"
    SURVIVAL = "生存"


# ---------------------------------------------------------------------------
# 实体数据类
# ---------------------------------------------------------------------------

@dataclass
class Monster:
    """怪物数据模型"""
    name: str
    level: int
    health: int
    attack: int
    defense: int
    special_abilities: List[str]
    loot: List[str]
    experience: int
    description: str = ""

    def take_damage(self, damage: int) -> bool:
        """受到伤害，返回是否死亡"""
        self.health -= damage
        return self.health <= 0


@dataclass
class Quest:
    """任务数据模型"""
    name: str
    description: str
    chapter: int
    requirements: Dict[str, int]
    rewards: Dict[str, int]
    morality_impact: Dict[str, int]

    def is_completed(self, player_progress: Dict[str, int]) -> bool:
        """检查任务是否完成"""
        for req, value in self.requirements.items():
            if player_progress.get(req, 0) < value:
                return False
        return True


@dataclass
class NPC:
    """NPC 数据模型"""
    name: str
    role: str
    personality: str
    relationship: int = 0  # -10 to 10
    available_quests: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class Dice:
    """骰子系统"""
    sides: int = 20

    def roll(self) -> int:
        """掷骰子"""
        return random.randint(1, self.sides)

    def roll_with_modifier(self, modifier: int = 0) -> int:
        """带修正值的骰子投掷"""
        return self.roll() + modifier


@dataclass
class Attribute:
    """角色属性数据模型"""
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    def get_modifier(self) -> Dict[ValueType, int]:
        """获取属性修正值"""
        return {
            ValueType.STRENGTH:     (self.strength     - 10) // 2,
            ValueType.DEXTERITY:    (self.dexterity    - 10) // 2,
            ValueType.CONSTITUTION: (self.constitution - 10) // 2,
            ValueType.INTELLIGENCE: (self.intelligence - 10) // 2,
            ValueType.WISDOM:       (self.wisdom       - 10) // 2,
            ValueType.CHARISMA:     (self.charisma     - 10) // 2,
        }

    def get_total(self, value_type: ValueType) -> int:
        """获取属性总值"""
        attributes = {
            ValueType.STRENGTH:     self.strength,
            ValueType.DEXTERITY:    self.dexterity,
            ValueType.CONSTITUTION: self.constitution,
            ValueType.INTELLIGENCE: self.intelligence,
            ValueType.WISDOM:       self.wisdom,
            ValueType.CHARISMA:     self.charisma,
        }
        return attributes[value_type]


@dataclass
class Morality:
    """道德值数据模型（-10 ~ +10，匹配游戏规则文档）"""
    light: int = 0
    shadow: int = 0
    balance: int = 0

    def add_light(self, amount: int):
        """增加光明值（-10 ~ +10范围）"""
        import game_systems
        import config
        self.light = game_systems.ExpandedMorality.clamp(self.light + amount)
        if amount > 0:
            self.balance = max(config.MORALITY_MIN, self.balance - amount // 2)

    def add_shadow(self, amount: int):
        """增加暗影值（-10 ~ +10范围）"""
        import game_systems
        import config
        self.shadow = game_systems.ExpandedMorality.clamp(self.shadow + amount)
        if amount > 0:
            self.balance = max(config.MORALITY_MIN, self.balance - amount // 2)

    def add_balance(self, amount: int):
        """增加平衡值（-10 ~ +10范围）"""
        import game_systems
        self.balance = game_systems.ExpandedMorality.clamp(self.balance + amount)

    def get_total(self) -> int:
        """获取道德值总和"""
        return self.light + self.shadow + self.balance

    def get_dominant_type(self) -> MoralityType:
        """获取主导道德类型"""
        if self.light >= self.shadow and self.light >= self.balance:
            return MoralityType.LIGHT
        elif self.shadow >= self.light and self.shadow >= self.balance:
            return MoralityType.SHADOW
        else:
            return MoralityType.BALANCE


@dataclass
class Skill:
    """技能数据模型"""
    name: str
    skill_type: SkillType
    level: int = 1
    description: str = ""

    def get_bonus(self, attributes: Attribute) -> int:
        """获取技能加值"""
        base_bonus = self.level
        modifier = 0

        if self.skill_type == SkillType.COMBAT:
            modifier = attributes.get_modifier()[ValueType.STRENGTH]
        elif self.skill_type == SkillType.STEALTH:
            modifier = attributes.get_modifier()[ValueType.DEXTERITY]
        elif self.skill_type == SkillType.MAGIC:
            modifier = attributes.get_modifier()[ValueType.INTELLIGENCE]
        elif self.skill_type == SkillType.SOCIAL:
            modifier = attributes.get_modifier()[ValueType.CHARISMA]
        elif self.skill_type == SkillType.SURVIVAL:
            modifier = attributes.get_modifier()[ValueType.WISDOM]

        return base_bonus + modifier


@dataclass
class Equipment:
    """装备数据模型"""
    name: str
    equipment_type: str
    rarity: str = "common"
    attack_bonus: int = 0
    defense_bonus: int = 0
    special_effect: str = ""
    description: str = ""

    def get_total_attack(self, user_attributes: Attribute) -> int:
        """获取攻击力加成"""
        return self.attack_bonus + user_attributes.get_modifier()[ValueType.STRENGTH]

    def get_total_defense(self, user_attributes: Attribute) -> int:
        """获取防御力加成"""
        return self.defense_bonus + user_attributes.get_modifier()[ValueType.DEXTERITY]


@dataclass
class Spell:
    """法术数据模型"""
    name: str
    spell_level: int
    school: str
    description: str
    damage_dice: str
    damage_type: str
    components: str = ""
    casting_time: str = "1 action"
    range: str = "30 feet"
    duration: str = "Instantaneous"

    def calculate_damage(self, target: Optional[Monster] = None) -> int:
        """计算法术伤害，考虑目标类型和伤害类型"""
        if not self.damage_dice:
            return 0

        try:
            dice_count, dice_type = self.damage_dice.split('d')
            base_damage = sum(
                random.randint(1, int(dice_type)) for _ in range(int(dice_count))
            )
        except Exception:
            return 0

        # 考虑法术等级加成
        base_damage += max(0, self.spell_level - 1)

        # 考虑目标抗性
        if target:
            base_damage = int(base_damage * self.get_damage_multiplier(target))

        return base_damage

    def get_damage_multiplier(self, target: Monster) -> float:
        """获取对目标伤害类型的乘数"""
        monster_damage_resistances = {
            "火焰精魄": {"冰冻": 2.0, "火焰": 0.5, "雷电": 1.0},
            "冰冻精魄": {"火焰": 2.0, "冰冻": 0.5, "雷电": 1.0},
            "雷电精魄": {"火焰": 1.0, "冰冻": 1.0, "雷电": 0.5},
            "暗影生物": {"光明": 0.5, "暗影": 1.5, "神圣": 2.0},
            "神圣生物": {"暗影": 2.0, "光明": 1.5, "神圣": 0.5},
            "元素生物": {"火焰": 1.0, "冰冻": 1.0, "雷电": 1.0},
        }

        target_type = next(
            (t for t in monster_damage_resistances if t in target.name), None
        )
        if target_type:
            return monster_damage_resistances[target_type].get(self.damage_type, 1.0)
        return 1.0

    def get_damage_effect(self) -> str:
        """获取伤害效果描述"""
        damage_effects = {
            "火焰": "灼烧伤害",
            "冰冻": "冰冻效果",
            "雷电": "麻痹效果",
            "光明": "净化效果",
            "暗影": "吸取生命",
            "神圣": "治愈效果",
            "治疗": "恢复生命",
            "毒素": "中毒效果",
            "穿刺": "贯通伤害",
            "钝击": "震荡伤害",
        }
        return damage_effects.get(self.damage_type, "伤害效果")
