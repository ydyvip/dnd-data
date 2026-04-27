"""
《暗影王座的救赎》DND游戏核心系统
基于之前创建的游戏规则实现的完整游戏引擎
"""

import json
import random
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from abc import ABC, abstractmethod


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


@dataclass
class Monster:
    """怪物"""
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
    """任务"""
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
    """NPC"""
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
    """角色属性"""
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    def get_modifier(self) -> Dict[ValueType, int]:
        """获取属性修正值"""
        return {
            ValueType.STRENGTH: (self.strength - 10) // 2,
            ValueType.DEXTERITY: (self.dexterity - 10) // 2,
            ValueType.CONSTITUTION: (self.constitution - 10) // 2,
            ValueType.INTELLIGENCE: (self.intelligence - 10) // 2,
            ValueType.WISDOM: (self.wisdom - 10) // 2,
            ValueType.CHARISMA: (self.charisma - 10) // 2
        }
    
    def get_total(self, value_type: ValueType) -> int:
        """获取属性总值"""
        attributes = {
            ValueType.STRENGTH: self.strength,
            ValueType.DEXTERITY: self.dexterity,
            ValueType.CONSTITUTION: self.constitution,
            ValueType.INTELLIGENCE: self.intelligence,
            ValueType.WISDOM: self.wisdom,
            ValueType.CHARISMA: self.charisma
        }
        return attributes[value_type]


@dataclass
class Morality:
    """道德值系统"""
    light: int = 0
    shadow: int = 0
    balance: int = 0
    
    def add_light(self, amount: int):
        """增加光明值"""
        self.light = min(10, self.light + amount)
        self.balance = max(0, self.balance - amount // 2)
        
    def add_shadow(self, amount: int):
        """增加暗影值"""
        self.shadow = min(10, self.shadow + amount)
        self.balance = max(0, self.balance - amount // 2)
        
    def add_balance(self, amount: int):
        """增加平衡值"""
        self.balance = min(10, self.balance + amount)
        
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
    """技能"""
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
    """装备"""
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
    """法术"""
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
        
        # 计算基础伤害
        try:
            dice_count, dice_type = self.damage_dice.split('d')
            base_damage = sum(random.randint(1, int(dice_type)) for _ in range(int(dice_count)))
        except:
            # 如果damage_dice格式不正确，返回0
            return 0
        
        # 考虑法术等级加成
        level_bonus = max(0, self.spell_level - 1)
        base_damage += level_bonus
        
        # 考虑目标抗性
        if target:
            damage_multiplier = self.get_damage_multiplier(target)
            base_damage = int(base_damage * damage_multiplier)
        
        return base_damage
    
    def get_damage_multiplier(self, target: Monster) -> float:
        """获取对目标伤害类型的乘数"""
        # 这里可以根据不同怪物类型设置不同的伤害抗性
        # 例如：火焰生物对火焰伤害有抗性，但弱冰冻伤害
        
        # 基础怪物类型与伤害类型的关联
        monster_damage_resistances = {
            "火焰精魄": {"冰冻": 2.0, "火焰": 0.5, "雷电": 1.0},
            "冰冻精魄": {"火焰": 2.0, "冰冻": 0.5, "雷电": 1.0},
            "雷电精魄": {"火焰": 1.0, "冰冻": 1.0, "雷电": 0.5},
            "暗影生物": {"光明": 0.5, "暗影": 1.5, "神圣": 2.0},
            "神圣生物": {"暗影": 2.0, "光明": 1.5, "神圣": 0.5},
            "元素生物": {"火焰": 1.0, "冰冻": 1.0, "雷电": 1.0}
        }
        
        # 获取目标类型的默认设置
        target_type = next((resist_type for resist_type in monster_damage_resistances 
                          if target.name.contains(resist_type)), None)
        
        if target_type and target_type in monster_damage_resistances:
            resistances = monster_damage_resistances[target_type]
            return resistances.get(self.damage_type, 1.0)
        
        # 默认没有特殊抗性
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
            "钝击": "震荡伤害"
        }
        
        return damage_effects.get(self.damage_type, "伤害效果")

class GameState(Enum):
    """游戏状态"""
    MENU = "菜单"
    CHARACTER_CREATION = "角色创建"
    EXPLORATION = "探索"
    COMBAT = "战斗"
    DIALOGUE = "对话"
    GAME_OVER = "游戏结束"
    CHAPTER_COMPLETE = "章节完成"


class Player:
    """玩家角色"""
    def __init__(self, name: str, background: str, character_class: str):
        self.name = name
        self.background = background
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.attributes = Attribute()
        self.morality = Morality()
        self.skills: List[Skill] = []
        self.equipment: List[Equipment] = []
        self.spells: List[Spell] = []
        self.health = 100
        self.max_health = 100
        self.current_chapter = 1
        self.gold = 100
        self.inventory: List[str] = []
        self.completed_quests: List[str] = []
        self.progress: Dict[str, int] = {}
        
        self.initialize_class()
    
    def initialize_class(self):
        """根据职业初始化角色"""
        # 简化的职业初始化
        if self.character_class == "战士":
            self.attributes.strength = 16
            self.attributes.constitution = 14
            self.skills.extend([
                Skill("剑术", SkillType.COMBAT, 1, "基础剑术技巧"),
                Skill("格挡", SkillType.COMBAT, 1, "防御技巧")
            ])
        elif self.character_class == "法师":
            self.attributes.intelligence = 16
            self.attributes.wisdom = 14
            self.spells.extend([
                Spell("火球术", SkillType.MAGIC, 1, "元素", "3d6火球伤害", "火"),
                Spell("治疗术", SkillType.MAGIC, 1, "神圣", "2d8治疗", "治疗")
            ])
        elif self.character_class == "牧师":
            self.attributes.wisdom = 16
            self.attributes.charisma = 14
            self.spells.extend([
                Spell("圣光术", SkillType.MAGIC, 1, "光明", "2d6光明伤害", "光明"),
                Spell("祝福", SkillType.MAGIC, 1, "神圣", "增加友军攻击力", "祝福")
            ])
        elif self.character_class == "游侠":
            self.attributes.dexterity = 16
            self.attributes.wisdom = 14
            self.skills.extend([
                Skill("弓术", SkillType.COMBAT, 1, "基础弓箭技巧"),
                Skill("潜行", SkillType.STEALTH, 1, "隐秘移动")
            ])
        elif self.character_class == "盗贼":
            self.attributes.dexterity = 16
            self.attributes.charisma = 14
            self.skills.extend([
                Skill("开锁", SkillType.STEALTH, 1, "开锁技巧"),
                Skill("偷窃", SkillType.STEALTH, 1, "灵巧偷窃")
            ])
    
    def gain_experience(self, exp: int):
        """获得经验值"""
        self.experience += exp
        self.check_level_up()
    
    def check_level_up(self):
        """检查是否升级"""
        required_exp = self.level * 1000
        if self.experience >= required_exp:
            self.level += 1
            self.experience -= required_exp
            self.max_health += 10
            self.health = self.max_health
            # 增加属性
            stat_increase = random.choice(list(ValueType))
            current_value = self.attributes.get_total(stat_increase)
            self.__setattr__(stat_increase.name.lower(), current_value + 2)
            
            return True
        return False
    
    def take_damage(self, damage: int):
        """受到伤害"""
        self.health = max(0, self.health - damage)
        return self.health <= 0
    
    def heal(self, amount: int):
        """恢复生命值"""
        self.health = min(self.max_health, self.health + amount)
    
    def equip_item(self, equipment: Equipment):
        """装备物品"""
        self.equipment.append(equipment)
    
    def learn_spell(self, spell: Spell):
        """学习法术"""
        self.spells.append(spell)
    
    def learn_skill(self, skill: Skill):
        """学习技能"""
        self.skills.append(skill)


class Chapter:
    """游戏章节"""
    def __init__(self, chapter_number: int, name: str, level_range: Tuple[int, int]):
        self.chapter_number = chapter_number
        self.name = name
        self.level_range = level_range
        self.quests: List[Quest] = []
        self.npcs: List[NPC] = []
        self.monsters: List[Monster] = []
        self.locations: List[str] = []
        self.final_boss: Optional[Monster] = None
        
    def add_quest(self, quest: Quest):
        """添加任务"""
        self.quests.append(quest)
        
    def add_npc(self, npc: NPC):
        """添加NPC"""
        self.npcs.append(npc)
        
    def add_monster(self, monster: Monster):
        """添加怪物"""
        self.monsters.append(monster)
        
    def add_location(self, location: str):
        """添加地点"""
        self.locations.append(location)


class Game:
    """游戏主类"""
    def __init__(self):
        self.player: Optional[Player] = None
        self.current_state = GameState.MENU
        self.current_chapter: Optional[Chapter] = None
        self.chapters: List[Chapter] = []
        self.backgrounds = self.load_json_backgrounds()
        self.character_classes = self.load_json_classes()
        self.equipment_database = self.load_json_equipment()
        self.spell_database = self.load_json_spells()
        self.monster_database = self.load_json_monsters()
        self.initialize_chapters()
        
    def load_json_data(self, file_path: str) -> List[Dict[str, Any]]:
        """加载JSON数据文件的通用方法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            print(f"⚠️ 文件未找到: {file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON解析错误 {file_path}: {e}")
            return []
        except Exception as e:
            print(f"⚠️ 加载文件 {file_path} 时发生错误: {e}")
            return []
    
    def load_json_backgrounds(self) -> List[str]:
        """从JSON文件加载背景数据"""
        data = self.load_json_data("data/backgrounds.json")
        return [item.get("name", "") for item in data if item.get("name")]
    
    def load_json_classes(self) -> List[str]:
        """从JSON文件加载职业数据"""
        data = self.load_json_data("data/classes.json")
        return [item.get("name", "") for item in data if item.get("name")]
    
    def load_json_equipment(self) -> List[Equipment]:
        """从JSON文件加载装备数据"""
        data = self.load_json_data("data/items.json")
        equipment_list = []
        
        for item in data:
            name = item.get("name", "")
            description = item.get("description", "")
            
            # 根据描述判断装备类型
            equipment_type = "其他"
            rarity = "common"
            
            if "武器" in description or "sword" in description.lower():
                equipment_type = "武器"
            elif "防具" in description or "armor" in description.lower() or "robe" in description.lower():
                equipment_type = "防具"
            elif "护符" in description or "amulet" in description.lower() or "ring" in description.lower():
                equipment_type = "饰品"
            
            # 根据描述判断稀有度
            if "rare" in description.lower():
                rarity = "rare"
            elif "uncommon" in description.lower():
                rarity = "uncommon"
            elif "legendary" in description.lower():
                rarity = "legendary"
            
            equipment = Equipment(
                name=name,
                equipment_type=equipment_type,
                rarity=rarity,
                attack_bonus=self.extract_attack_bonus(description),
                defense_bonus=self.extract_defense_bonus(description),
                special_effect=self.extract_special_effect(item.get("properties", {})),
                description=description
            )
            equipment_list.append(equipment)
        
        return equipment_list
    
    def load_json_spells(self) -> List[Spell]:
        """从JSON文件加载法术数据"""
        data = self.load_json_data("data/spells.json")
        spells_list = []
        
        for item in data:
            name = item.get("name", "")
            description = item.get("description", "")
            
            # 从描述中提取法术信息
            level = self.extract_spell_level(description)
            school = self.extract_spell_school(description)
            damage = self.extract_spell_damage(description)
            morality_type = self.extract_spell_morality(description)
            
            spell = Spell(
                name=name,
                spell_level=level,
                school=school,
                description=description,
                damage_dice=damage,
                damage_type=morality_type,
                components="V,S",
                casting_time="1动作",
                range="60尺",
                duration="瞬间"
            )
            spells_list.append(spell)
        
        return spells_list
    
    def load_json_monsters(self) -> List[Monster]:
        """从JSON文件加载怪物数据"""
        data = self.load_json_data("data/monsters.json")
        monsters_list = []
        
        for item in data:
            name = item.get("name", "")
            description = item.get("description", "")
            
            # 根据描述估算怪物属性
            level = self.extract_monster_level(description)
            health = self.extract_monster_health(description, level)
            attack = self.extract_monster_attack(description, level)
            defense = self.extract_monster_defense(description, level)
            
            monster = Monster(
                name=name,
                level=level,
                health=health,
                attack=attack,
                defense=defense,
                special_abilities=self.extract_monster_abilities(description),
                loot=self.extract_monster_loot(description),
                experience=level * 100,
                description=description
            )
            monsters_list.append(monster)
        
        return monsters_list
    
    # 辅助方法：从文本中提取特定信息
    def extract_attack_bonus(self, description: str) -> int:
        """从描述中提取攻击加值"""
        # 简单的提取逻辑，可以根据需要改进
        if "+1" in description:
            return 1
        elif "+2" in description:
            return 2
        elif "+3" in description:
            return 3
        return 0
    
    def extract_defense_bonus(self, description: str) -> int:
        """从描述中提取防御加值"""
        # 简单的提取逻辑，可以根据需要改进
        if "+1" in description:
            return 1
        elif "+2" in description:
            return 2
        elif "+3" in description:
            return 3
        return 0
    
    def extract_spell_level(self, description: str) -> int:
        """从描述中提取法术等级"""
        import re
        match = re.search(r'(\d+)级', description)
        if match:
            return int(match.group(1))
        
        # 英文匹配
        match = re.search(r'(\d+)st level|(\d+)nd level|(\d+)rd level|(\d+)th level', description)
        if match:
            for group in match.groups():
                if group and group.isdigit():
                    return int(group)
        
        return 0  # 默认为戏法
    
    def extract_spell_school(self, description: str) -> str:
        """从描述中提取法术学派"""
        schools = ["预言", "塑能", "防护", "咒法", "幻术", "死灵", "变化", "光明", "暗影", "元素"]
        for school in schools:
            if school in description:
                return school
        return "通用"
    
    def extract_spell_damage(self, description: str) -> str:
        """从描述中提取伤害描述"""
        import re
        # 匹配伤害骰子如 1d4, 2d6, 6d8 等
        damage_pattern = r'(\d+)d(\d+)'
        match = re.search(damage_pattern, description)
        if match:
            return f"{match.group(1)}d{match.group(2)}伤害"
        return "特殊效果"
    
    def extract_spell_morality(self, description: str) -> str:
        """从描述中提取道德类型"""
        if "光明" in description or "神圣" in description or "治愈" in description:
            return "光明"
        elif "暗影" in description or "黑暗" in description or "诅咒" in description:
            return "暗影"
        return "平衡"
    
    def extract_monster_level(self, description: str) -> int:
        """从描述中提取怪物等级"""
        import re
        match = re.search(r'(\d+)级', description)
        if match:
            return int(match.group(1))
        return 1  # 默认等级
    
    def extract_monster_health(self, description: str, level: int) -> int:
        """从描述中提取怪物生命值"""
        # 基础生命值计算
        base_health = 6 + (level * 2)
        
        # 根据描述调整
        if "强大" in description or "strong" in description.lower():
            base_health += 10
        elif "虚弱" in description or "weak" in description.lower():
            base_health -= 3
        
        return max(1, base_health)
    
    def extract_monster_attack(self, description: str, level: int) -> int:
        """从描述中提取怪物攻击力"""
        return 3 + level
    
    def extract_monster_defense(self, description: str, level: int) -> int:
        """从描述中提取怪物防御力"""
        return 2 + level
    
    def extract_monster_abilities(self, description: str) -> List[str]:
        """从描述中提取怪物特殊能力"""
        abilities = []
        if "喷吐" in description:
            abilities.append("龙息攻击")
        if "飞行" in description:
            abilities.append("飞行")
        if "隐形" in description:
            abilities.append("隐形")
        if "毒素" in description:
            abilities.append("毒素攻击")
        return abilities if abilities else ["基础攻击"]
    
    def extract_monster_loot(self, description: str) -> List[str]:
        """从描述中提取怪物战利品"""
        loot = []
        if "金币" in description or "gold" in description.lower():
            loot.append("金币")
        if "宝石" in description:
            loot.append("宝石")
        if "魔法物品" in description or "magic" in description.lower():
            loot.append("魔法物品")
        return loot if loot else ["普通战利品"]
    
    def extract_special_effect(self, properties: Dict[str, Any]) -> str:
        """从属性字典中提取特殊效果描述"""
        if not properties:
            return ""
        
        effect_parts = []
        if properties.get("Category"):
            effect_parts.append(f"{properties.get('Category')}")
        if properties.get("Item Type"):
            effect_parts.append(f"{properties.get('Item Type')}")
        if properties.get("Item Rarity"):
            effect_parts.append(f"{properties.get('Item Rarity')}")
        
        return ", ".join(effect_parts) if effect_parts else ""

    def generate_backgrounds(self) -> List[str]:
        """生成背景列表 - 优先使用JSON数据，fallback到内置数据"""
        json_backgrounds = self.load_json_backgrounds()
        if json_backgrounds:
            return json_backgrounds
        
        # fallback到原始数据
        return [
            "孤儿", "贵族", "冒险者", "农夫", "商人", "学者", "士兵", 
            "牧师", "盗贼", "吟游诗人", "工匠", "猎人", "流浪者", "难民"
        ]
    
    def generate_classes(self) -> List[str]:
        """生成职业列表 - 优先使用JSON数据，fallback到内置数据"""
        json_classes = self.load_json_classes()
        if json_classes:
            return json_classes
        
        # fallback到原始数据
        return ["战士", "法师", "牧师", "游侠", "盗贼", "圣武士", "野蛮人", 
                "德鲁伊", "术士", "武僧", "吟游诗人", "邪术师"]
    
    def generate_equipment(self) -> List[Equipment]:
        """生成装备数据库 - 优先使用JSON数据，fallback到内置数据"""
        json_equipment = self.load_json_equipment()
        if json_equipment:
            return json_equipment
        
        # fallback到原始数据
        return [
            Equipment("长剑", "武器", "common", 2, 0, "基础剑类武器", "一把标准的长剑"),
            Equipment("短弓", "武器", "common", 1, 0, "基础弓类武器", "一把简单的短弓"),
            Equipment("皮甲", "防具", "common", 0, 2, "基础防具", "轻便的皮制护甲"),
            Equipment("法师袍", "防具", "common", 0, 1, "增加法术效果", "舒适的法师长袍"),
            Equipment("神圣护符", "饰品", "rare", 1, 1, "增加神圣法术效果", "闪烁着神圣光芒的护符"),
            Equipment("暗影匕首", "武器", "uncommon", 1, 0, "在暗影中造成额外伤害", "一把散发着暗影气息的匕首"),
            Equipment("平衡戒指", "饰品", "legendary", 0, 0, "平衡光明与暗影力量", "古老而神秘的戒指")
        ]
    
    def generate_spells(self) -> List[Spell]:
        """生成法术数据库 - 优先使用JSON数据，fallback到内置数据"""
        json_spells = self.load_json_spells()
        if json_spells:
            return json_spells
        
        # fallback到原始数据
        return [
            Spell("光明术", 0, "光明", "1d4光明伤害", "光明", "V,S", "1动作", "60尺", "瞬间"),
            Spell("暗影术", 0, "暗影", "1d4暗影伤害", "暗影", "V,S", "1动作", "60尺", "瞬间"),
            Spell("火球术", 2, "元素", "6d6火球伤害", "火", "V,S,M", "1动作", "150尺", "瞬间"),
            Spell("治疗术", 1, "神圣", "2d8治疗", "治疗", "V,S", "1动作", "接触", "瞬间"),
            Spell("圣光术", 1, "光明", "2d6光明伤害", "光明", "V,S", "1动作", "60尺", "持续1分钟"),
            Spell("暗影箭", 1, "暗影", "2d8暗影伤害", "暗影", "V,S", "1动作", "120尺", "瞬间"),
            Spell("净化之光", 3, "神圣", "大范围净化", "神圣", "V,S,SM", "10分钟", "30尺", "持续1分钟"),
            Spell("暗影风暴", 3, "暗影", "大范围暗影伤害", "暗影", "V,S,SM", "10分钟", "100尺", "持续1分钟"),
            Spell("创世纪", 9, "创世", "创造新的世界", "创世", "V,S,SM", "1小时", "无限", "永久"),
            Spell("神圣终结", 9, "神圣", "终极神圣法术", "神圣", "V,S,SM", "1小时", "无限", "永久")
        ]
    
    def generate_monsters(self) -> List[Monster]:
        """生成怪物数据库 - 优先使用JSON数据，fallback到内置数据"""
        json_monsters = self.load_json_monsters()
        if json_monsters:
            return json_monsters
        
        # fallback到原始数据
        return [
            Monster("哥布林", 1, 15, 8, 10, ["偷袭"], ["铜币", "短剑"], 50),
            Monster("骷髅战士", 2, 25, 12, 12, ["不死"], ["骨头", "破旧武器"], 100),
            Monster("暗影生物", 3, 30, 15, 8, ["暗影适应", "恐惧"], ["暗影碎片", "暗影武器"], 150),
            Monster("元素精魄", 4, 40, 18, 14, ["元素攻击", "元素抗性"], ["元素晶体", "魔法物品"], 200),
            Monster("古代守护者", 5, 60, 20, 18, ["古代知识", "守护"], ["古代遗物", "神秘物品"], 300),
            Monster("暗影君主", 20, 200, 25, 20, ["暗影掌控", "灵魂汲取", "时空扭曲"], ["暗影王座", "暗影之心"], 10000)
        ]
    
    def initialize_chapters(self):
        """初始化游戏章节"""
        # 第一章：边境村庄
        chapter1 = Chapter(1, "边境村庄", (1, 5))
        chapter1.add_location("村庄广场")
        chapter1.add_location("神殿")
        chapter1.add_location("铁匠铺")
        chapter1.add_location("酒馆")
        chapter1.add_monster(self.monster_database[0])  # 哥布林
        chapter1.add_monster(self.monster_database[1])  # 骷髅战士
        
        # 第二章：暗影森林
        chapter2 = Chapter(2, "暗影森林", (6, 10))
        chapter2.add_location("森林入口")
        chapter2.add_location("污染湖泊")
        chapter2.add_location("精灵村落")
        chapter2.add_location("古老树屋")
        chapter2.add_monster(self.monster_database[2])  # 暗影生物
        chapter2.add_monster(self.monster_database[3])  # 元素精魄
        
        # 第三章：古代遗迹
        chapter3 = Chapter(3, "古代遗迹", (11, 15))
        chapter3.add_location("遗迹外围")
        chapter3.add_location("中庭广场")
        chapter3.add_location("主神殿")
        chapter3.add_location("密室区域")
        chapter3.add_monster(self.monster_database[4])  # 古代守护者
        
        # 第四章：暗影王座
        chapter4 = Chapter(4, "暗影王座", (16, 20))
        chapter4.add_location("暗影王座外围")
        chapter4.add_location("暗影王座大殿")
        chapter4.add_location("暗影王座密室")
        chapter4.final_boss = self.monster_database[5]  # 暗影君主
        
        self.chapters = [chapter1, chapter2, chapter3, chapter4]
    
    def create_player(self, name: str, background: str, character_class: str):
        """创建玩家角色"""
        self.player = Player(name, background, character_class)
        self.current_state = GameState.EXPLORATION
        self.current_chapter = self.chapters[0]
        
    def start_new_game(self):
        """开始新游戏"""
        self.current_state = GameState.MENU
        self.player = None
        
    def get_current_chapter(self) -> Optional[Chapter]:
        """获取当前章节"""
        if self.player and 1 <= self.player.current_chapter <= len(self.chapters):
            return self.chapters[self.player.current_chapter - 1]
        return None
    
    def next_chapter(self):
        """进入下一章节"""
        if self.player and self.player.current_chapter < len(self.chapters):
            self.player.current_chapter += 1
            self.current_chapter = self.chapters[self.player.current_chapter - 1]
            self.player.health = self.player.max_health  # 恢复满生命值
    
    def check_morality_ending(self):
        """检查道德结局"""
        if self.player:
            if self.player.morality.light >= 8:
                return "光明救赎结局 - 你选择了光明的道路，净化了暗影王座，世界迎来了光明的新时代。"
            elif self.player.morality.shadow >= 8:
                return "黑暗统治结局 - 你选择了暗影的力量，成为了新的暗影君主，世界陷入了黑暗。"
            elif (self.player.morality.light >= 4 and self.player.morality.light <= 7 and 
                  self.player.morality.shadow >= 4 and self.player.morality.shadow <= 7):
                return "平衡之道结局 - 你找到了光明与暗影的平衡，世界进入了新的和谐时代。"
        return "游戏结束"
    
    def complete_game(self):
        """完成游戏"""
        self.current_state = GameState.GAME_OVER
        ending = self.check_morality_ending()
        return ending


class GameEngine:
    """游戏引擎 - 提供游戏逻辑和界面控制"""
    
    def __init__(self):
        self.game = Game()
        self.dice = Dice(20)
        
    def create_character(self, name: str, background: str, character_class: str) -> bool:
        """创建角色"""
        if not name or not background or not character_class:
            return False
            
        self.game.create_player(name, background, character_class)
        return True
    
    def roll_dice(self, modifier: int = 0) -> int:
        """掷骰子"""
        return self.dice.roll_with_modifier(modifier)
    
    def combat_round(self, player_action: str, target: Monster) -> Dict[str, Any]:
        """战斗回合"""
        if not self.game.player or not target:
            return {"error": "无效的战斗参数"}
            
        result = {
            "player_action": player_action,
            "target_name": target.name,
            "player_attack": 0,
            "target_attack": 0,
            "player_damage": 0,
            "target_damage": 0,
            "target_alive": True,
            "player_alive": True
        }
        
        # 玩家攻击
        player_attack_roll = self.roll_dice(self.game.player.attributes.get_modifier()[ValueType.STRENGTH])
        player_equipment_bonus = sum(eq.attack_bonus for eq in self.game.player.equipment)
        result["player_attack"] = player_attack_roll + player_equipment_bonus
        
        if player_attack_roll > target.defense:
            damage = self.roll_dice(3) + player_equipment_bonus
            result["player_damage"] = damage
            
            if target.take_damage(damage):
                result["target_alive"] = False
                
        # 怪物反击
        if result["target_alive"]:
            target_attack_roll = self.roll_dice(target.attack)
            player_defense = self.game.player.attributes.get_modifier()[ValueType.DEXTERITY]
            player_armor_bonus = sum(eq.defense_bonus for eq in self.game.player.equipment)
            result["target_attack"] = target_attack_roll
            
            if target_attack_roll > player_defense + player_armor_bonus:
                monster_damage = self.roll_dice(2)
                result["target_damage"] = monster_damage
                
                if self.game.player.take_damage(monster_damage):
                    result["player_alive"] = False
                    
        return result
    
    def cast_spell(self, spell_name: str, target: Optional[Monster] = None) -> Dict[str, Any]:
        """施放法术"""
        if not self.game.player:
            return {"error": "没有玩家角色"}
            
        spell = next((s for s in self.game.player.spells if s.name == spell_name), None)
        if not spell:
            return {"error": f"未找到法术：{spell_name}"}
            
        result = {
            "spell_name": spell_name,
            "spell_level": spell.spell_level,
            "damage": 0,
            "effect": spell.description
        }
        
        if spell.damage_dice:
            result["damage"] = spell.calculate_damage()
            
            if target and result["damage"] > 0:
                if target.take_damage(result["damage"]):
                    result["effect"] = f"{target.name}被击败了！"
                    
        return result
    
    def use_skill(self, skill_name: str) -> Dict[str, Any]:
        """使用技能"""
        if not self.game.player:
            return {"error": "没有玩家角色"}
            
        skill = next((s for s in self.game.player.skills if s.name == skill_name), None)
        if not skill:
            return {"error": f"未找到技能：{skill_name}"}
            
        skill_bonus = skill.get_bonus(self.game.player.attributes)
        result = {
            "skill_name": skill_name,
            "skill_level": skill.level,
            "bonus": skill_bonus,
            "result": self.roll_dice(skill_bonus),
            "description": skill.description
        }
        
        return result
    
    def make_morality_choice(self, choice_type: str, amount: int) -> Dict[str, Any]:
        """做出道德选择"""
        if not self.game.player:
            return {"error": "没有玩家角色"}
            
        if choice_type == "light":
            self.game.player.morality.add_light(amount)
            result_type = "光明"
        elif choice_type == "shadow":
            self.game.player.morality.add_shadow(amount)
            result_type = "暗影"
        elif choice_type == "balance":
            self.game.player.morality.add_balance(amount)
            result_type = "平衡"
        else:
            return {"error": "无效的道德选择类型"}
            
        return {
            "choice_type": result_type,
            "amount": amount,
            "current_values": {
                "light": self.game.player.morality.light,
                "shadow": self.game.player.morality.shadow,
                "balance": self.game.player.morality.balance
            }
        }
    
    def equip_item(self, equipment_name: str) -> Dict[str, Any]:
        """装备物品"""
        if not self.game.player:
            return {"error": "没有玩家角色"}
            
        equipment = next((eq for eq in self.game.equipment_database if eq.name == equipment_name), None)
        if not equipment:
            return {"error": f"未找到装备：{equipment_name}"}
            
        self.game.player.equip_item(equipment)
        
        return {
            "item_equipped": equipment_name,
            "attack_bonus": equipment.attack_bonus,
            "defense_bonus": equipment.defense_bonus,
            "special_effect": equipment.special_effect
        }
    
    def complete_quest(self, quest_name: str) -> Dict[str, Any]:
        """完成任务"""
        if not self.game.player:
            return {"error": "没有玩家角色"}
            
        chapter = self.game.get_current_chapter()
        if not chapter:
            return {"error": "当前章节无效"}
            
        quest = next((q for q in chapter.quests if q.name == quest_name), None)
        if not quest:
            return {"error": f"未找到任务：{quest_name}"}
            
        if not quest.is_completed(self.game.player.progress):
            return {"error": "任务要求未完成"}
            
        # 给予奖励
        self.game.player.completed_quests.append(quest_name)
        self.game.player.gain_experience(quest.rewards.get("experience", 0))
        
        # 应用道德影响
        for morality_type, amount in quest.morality_impact.items():
            if morality_type == "light":
                self.game.player.morality.add_light(amount)
            elif morality_type == "shadow":
                self.game.player.morality.add_shadow(amount)
            elif morality_type == "balance":
                self.game.player.morality.add_balance(amount)
        
        return {
            "quest_completed": quest_name,
            "experience_gained": quest.rewards.get("experience", 0),
            "morality_impact": quest.morality_impact
        }
    
    def get_player_status(self) -> Dict[str, Any]:
        """获取玩家状态"""
        if not self.game.player:
            return {"error": "没有玩家角色"}
            
        return {
            "name": self.game.player.name,
            "level": self.game.player.level,
            "experience": self.game.player.experience,
            "health": self.game.player.health,
            "max_health": self.game.player.max_health,
            "gold": self.game.player.gold,
            "current_chapter": self.game.player.current_chapter,
            "attributes": {
                "strength": self.game.player.attributes.strength,
                "dexterity": self.game.player.attributes.dexterity,
                "constitution": self.game.player.attributes.constitution,
                "intelligence": self.game.player.attributes.intelligence,
                "wisdom": self.game.player.attributes.wisdom,
                "charisma": self.game.player.attributes.charisma
            },
            "morality": {
                "light": self.game.player.morality.light,
                "shadow": self.game.player.morality.shadow,
                "balance": self.game.player.morality.balance
            },
            "equipment": [eq.name for eq in self.game.player.equipment],
            "skills": [skill.name for skill in self.game.player.skills],
            "spells": [spell.name for spell in self.game.player.spells]
        }
    
    def get_current_chapter_info(self) -> Dict[str, Any]:
        """获取当前章节信息"""
        chapter = self.game.get_current_chapter()
        if not chapter:
            return {"error": "当前章节无效"}
            
        return {
            "chapter_number": chapter.chapter_number,
            "name": chapter.name,
            "level_range": chapter.level_range,
            "locations": chapter.locations,
            "npcs": [npc.name for npc in chapter.npcs],
            "monsters": [monster.name for monster in chapter.monsters],
            "quests": [quest.name for quest in chapter.quests]
        }


# 简单的控制台游戏演示
def console_game_demo():
    """控制台游戏演示"""
    engine = GameEngine()
    
    print("=== 《暗影王座的救赎》游戏演示 ===")
    print("欢迎来到暗影王座的救赎！")
    
    # 创建角色
    print("\n--- 创建角色 ---")
    name = input("请输入角色名称: ")
    background = input("请选择背景 (孤儿/贵族/冒险者): ")
    character_class = input("请选择职业 (战士/法师/牧师/游侠/盗贼): ")
    
    if engine.create_character(name, background, character_class):
        print(f"角色 {name} 创建成功！")
        
        # 显示角色状态
        status = engine.get_player_status()
        print(f"\n角色状态:")
        print(f"等级: {status['level']}")
        print(f"职业: {character_class}")
        print(f"生命值: {status['health']}/{status['max_health']}")
        print(f"道德值: 光明={status['morality']['light']}, 暗影={status['morality']['shadow']}, 平衡={status['morality']['balance']}")
    else:
        print("角色创建失败！")
        return
    
    # 进入游戏
    input("\n按Enter键开始冒险...")
    
    # 模拟简单的游戏流程
    while True:
        print("\n=== 游戏菜单 ===")
        print("1. 查看角色状态")
        print("2. 进行战斗")
        print("3. 使用法术")
        print("4. 使用技能")
        print("5. 做出道德选择")
        print("6. 装备物品")
        print("7. 完成任务")
        print("8. 下一章节")
        print("9. 游戏结束")
        
        choice = input("请选择操作 (1-9): ")
        
        if choice == "1":
            status = engine.get_player_status()
            print(f"\n角色状态:")
            print(f"名称: {status['name']}")
            print(f"等级: {status['level']}")
            print(f"经验: {status['experience']}")
            print(f"生命值: {status['health']}/{status['max_health']}")
            print(f"金币: {status['gold']}")
            print(f"当前章节: {status['current_chapter']}")
            print(f"道德值: 光明={status['morality']['light']}, 暗影={status['morality']['shadow']}, 平衡={status['morality']['balance']}")
            print(f"装备: {', '.join(status['equipment'])}")
            print(f"技能: {', '.join(status['skills'])}")
            print(f"法术: {', '.join(status['spells'])}")
            
        elif choice == "2":
            chapter = engine.get_current_chapter_info()
            if chapter['monsters']:
                monster_name = chapter['monsters'][0]
                print(f"遇到 {monster_name}！")
                
                combat_result = engine.combat_round("攻击", engine.game.monster_database[0])
                print(f"战斗结果:")
                print(f"攻击检定: {combat_result['player_attack']}")
                print(f"造成伤害: {combat_result['player_damage']}")
                print(f"剩余生命: {combat_result['target_alive']}")
                
                if combat_result['target_damage'] > 0:
                    print(f"受到伤害: {combat_result['target_damage']}")
                    
                if not combat_result['player_alive']:
                    print("你被击败了！游戏结束。")
                    break
                    
            else:
                print("当前章节没有可战斗的怪物。")
                
        elif choice == "3":
            if engine.game.player.spells:
                print(f"可用法术: {', '.join([spell.name for spell in engine.game.player.spells])}")
                spell_name = input("请选择要使用的法术: ")
                result = engine.cast_spell(spell_name)
                print(f"法术结果: {result}")
            else:
                print("你没有学会任何法术。")
                
        elif choice == "4":
            if engine.game.player.skills:
                print(f"可用技能: {', '.join([skill.name for skill in engine.game.player.skills])}")
                skill_name = input("请选择要使用的技能: ")
                result = engine.use_skill(skill_name)
                print(f"技能结果: {result}")
            else:
                print("你没有学会任何技能。")
                
        elif choice == "5":
            print("道德选择:")
            print("1. 做出光明选择 (+2光明值)")
            print("2. 做出暗影选择 (+2暗影值)")
            print("3. 做出平衡选择 (+2平衡值)")
            
            choice2 = input("请选择 (1-3): ")
            if choice2 == "1":
                result = engine.make_morality_choice("light", 2)
            elif choice2 == "2":
                result = engine.make_morality_choice("shadow", 2)
            elif choice2 == "3":
                result = engine.make_morality_choice("balance", 2)
            else:
                print("无效选择。")
                continue
                
            print(f"道德选择结果:")
            print(f"获得 {result['choice_type']}值 {result['amount']}")
            print(f"当前道德值: {result['current_values']}")
            
        elif choice == "6":
            print(f"可用装备: {', '.join([eq.name for eq in engine.game.equipment_database])}")
            equipment_name = input("请选择要装备的物品: ")
            result = engine.equip_item(equipment_name)
            print(f"装备结果: {result}")
            
        elif choice == "7":
            chapter = engine.get_current_chapter_info()
            if chapter['quests']:
                print(f"可用任务: {', '.join(chapter['quests'])}")
                quest_name = input("请选择要完成的任务: ")
                result = engine.complete_quest(quest_name)
                print(f"任务结果: {result}")
            else:
                print("当前章节没有可完成的任务。")
                
        elif choice == "8":
            current_chapter = engine.game.player.current_chapter
            if current_chapter < len(engine.game.chapters):
                engine.next_chapter()
                print(f"进入第 {engine.game.player.current_chapter} 章: {engine.game.current_chapter.name}")
            else:
                print("已经是最后一章了。")
                
        elif choice == "9":
            ending = engine.complete_game()
            print(f"\n{ending}")
            break
            
        else:
            print("无效选择。")


if __name__ == "__main__":
    # 运行控制台演示
    console_game_demo()