# -*- coding: utf-8 -*-
"""
《暗影王座的救赎》游戏子系统模块
包含：扩展道德系统、技能树、环境战斗、团队组合技、BOSS阶段、装备套装、法术协同、持久化

遵循设计文档：结局判定系统.md、战斗规则补充.md、法术和技能手册.md
"""

import json
import os
import random
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field

import config
from models import MoralityType, SkillType, NPC, Morality, Equipment, Spell


# ============================================================
# 1. 扩展道德系统 (匹配结局判定系统.md)
# ============================================================

class ExpandedMorality:
    """
    扩展道德系统：
    - 支持 -10 ~ +10 范围
    - 法术效果修正（光明高→神圣法术+2，暗影高→暗影法术+2，平衡高→所有+1）
    - 道德值影响对话解锁
    - NPC关系基于道德倾向的自动修正
    """

    @staticmethod
    def clamp(value: int) -> int:
        """将道德值限制在配置范围内"""
        return max(config.MORALITY_MIN, min(config.MORALITY_MAX, value))

    @staticmethod
    def get_spell_damage_modifier(morality: Morality, damage_type: str) -> int:
        """
        根据道德值返回法术伤害修正值
        光明值高→增强光明/神圣法术
        暗影值高→增强暗影法术
        平衡值高→所有法术微增
        """
        modifier = 0
        high_light = morality.light >= config.MORALITY_SPELL_BONUS_THRESHOLD
        high_shadow = morality.shadow >= config.MORALITY_SPELL_BONUS_THRESHOLD
        high_balance = morality.balance >= config.MORALITY_SPELL_BONUS_THRESHOLD

        if high_light and damage_type in ("光明", "神圣"):
            modifier += config.MORALITY_LIGHT_SPELL_BONUS
        if high_shadow and damage_type in ("暗影", "诅咒"):
            modifier += config.MORALITY_SHADOW_SPELL_BONUS
        if high_balance:
            modifier += config.MORALITY_BALANCE_SPELL_BONUS

        # 道德冲突：双方都高时根据主导类型调整
        if high_light and high_shadow:
            dominant = morality.get_dominant_type()
            if dominant == MoralityType.LIGHT:
                modifier += 1  # 光明主导额外+1
            elif dominant == MoralityType.SHADOW:
                modifier += 1  # 暗影主导额外+1
            # 平衡主导时，冲突缓和对双方都有利

        return modifier

    @staticmethod
    def get_available_dialogue_types(morality: Morality) -> List[str]:
        """
        根据道德值返回可用的对话选项类型
        返回可能的选项：["善良", "邪恶", "理性"]
        """
        available = []
        if morality.light >= config.MORALITY_DIALOGUE_GOOD_THRESHOLD:
            available.append("善良")
        if morality.shadow >= config.MORALITY_DIALOGUE_EVIL_THRESHOLD:
            available.append("邪恶")
        if morality.balance >= config.MORALITY_DIALOGUE_NEUTRAL_THRESHOLD:
            available.append("理性")
        # 道德值混合时解锁复杂选项
        if len(available) >= 2:
            available.append("复杂")
        return available

    @staticmethod
    def get_npc_relationship_modifier(morality: Morality, npc: NPC) -> int:
        """
        返回NPC关系修正值
        道德匹配→关系+2，道德冲突→关系-2
        """
        if npc.relationship > 0:
            # 友好NPC：倾向匹配道德
            if npc.relationship > 5:
                return 2  # 非常友好NPC自动+2
            return 1
        elif npc.relationship < 0:
            # 敌对NPC：倾向冲突道德
            return -2
        return 0

    @staticmethod
    def evaluate_morality_action(morality: Morality, action_type: str, impact: str) -> Dict[str, int]:
        """
        评估道德行动对三维道德的影响
        action_type: "saving" / "helping" / "sacrifice" / "forgiving" / 
                      "harming" / "betray" / "power" / "compromise" / "rational"
        impact: "major" / "normal" / "minor"
        """
        changes = {"light": 0, "shadow": 0, "balance": 0}
        impact_mult = {"major": 3, "normal": 2, "minor": 1}

        action_effects = {
            # 光明系
            "saving":    {"light": 2, "shadow": -1, "balance": 0},
            "helping":   {"light": 1, "shadow": 0, "balance": 0},
            "sacrifice": {"light": 3, "shadow": -2, "balance": -1},
            "forgiving": {"light": 1, "shadow": -1, "balance": 2},
            # 暗影系
            "power":     {"light": -1, "shadow": 2, "balance": 0},
            "harming":   {"light": 0, "shadow": 1, "balance": -1},
            "betray":    {"light": -2, "shadow": 3, "balance": -1},
            # 平衡系
            "compromise": {"light": 1, "shadow": 0, "balance": 2},
            "rational":  {"light": 0, "shadow": -1, "balance": 1}
        }

        if action_type in action_effects:
            mult = impact_mult.get(impact, 1)
            base = action_effects[action_type]
            for key in ("light", "shadow", "balance"):
                changes[key] = base.get(key, 0) * mult

        return changes


# ============================================================
# 2. 技能树系统 (5级技能进阶)
# ============================================================

@dataclass
class SkillTreeNode:
    """技能树节点"""
    name: str                             # 技能名称
    skill_type: SkillType                 # 技能类型
    max_level: int = 5                    # 最高等级
    description: str = ""                 # 描述
    prerequisites: List[str] = field(default_factory=list)  # 前置技能
    parent_skill: Optional[str] = None    # 父技能
    level_descriptions: Dict[int, str] = field(default_factory=dict)  # 每级描述

    def get_bonus_at_level(self, level: int) -> int:
        """获取指定等级的技能加值"""
        return level  # 基础加值 = 等级

    def can_advance_to(self, level: int, owned_skills: Dict[str, int],
                       player_level: int) -> Tuple[bool, str]:
        """检查是否能升级到指定等级"""
        if level > self.max_level:
            return False, "已达最高等级"

        # 等级要求：1级技能需玩家≥1，5级需玩家≥5
        required_player_level = level
        if player_level < required_player_level:
            return False, f"需要玩家等级 {required_player_level}"

        # 前置技能检查
        for prereq in self.prerequisites:
            prereq_level = owned_skills.get(prereq, 0)
            if prereq_level < 1:
                return False, f"需要前置技能: {prereq}"

        return True, ""
    
    # TODO
    def get_level_bonus(self, level: int):
        
        return level * 1.2


class SkillTree:
    """
    5级技能进阶系统
    技能树示例：
    剑术(Lv1) → 精通剑术(Lv3) → 大师剑术(Lv5)
    防御(Lv1) → 铁壁(Lv3) → 不败(Lv5)
    """

    # 预定义技能树结构
    DEFAULT_TREES = {
        "战斗系": {
            "剑术": SkillTreeNode("剑术", SkillType.COMBAT, 5, "基础剑术进阶之路",
                                 level_descriptions={
                                     1: "基础剑术：攻击+1",
                                     2: "熟练剑术：攻击+2",
                                     3: "精通剑术：攻击+3，获得顺势斩",
                                     4: "大师剑术：攻击+4，反击+1",
                                     5: "剑圣：攻击+5，终极剑技"
                                 }),
            "防御": SkillTreeNode("防御", SkillType.COMBAT, 5, "防御技巧进阶",
                                level_descriptions={
                                    1: "基础格挡：防御+1",
                                    2: "稳固防守：防御+2",
                                    3: "铁壁防御：防御+3，获得盾墙",
                                    4: "大师防御：防御+4，反击+2",
                                    5: "不败防御：防御+5，终极守护"
                                }),
            "弓术": SkillTreeNode("弓术", SkillType.COMBAT, 5, "远程武器精通",
                                 prerequisites=["剑术"],
                                 level_descriptions={
                                     1: "基础弓术：远程攻击+1",
                                     2: "精准射击：远程攻击+2",
                                     3: "快速射击：远程攻击+3，额外射击",
                                     4: "大师弓术：远程攻击+4，贯穿",
                                     5: "神射手：远程攻击+5，必中"
                                 }),
        },
        "魔法系": {
            "元素掌控": SkillTreeNode("元素掌控", SkillType.MAGIC, 5, "元素魔法进阶",
                                     level_descriptions={
                                         1: "元素感知：法术伤害+1",
                                         2: "元素亲和：法术伤害+2",
                                         3: "元素支配：法术伤害+3，双元素",
                                         4: "元素大师：法术伤害+4，施法加速",
                                         5: "元素之巅：法术伤害+5，终极元素"
                                     }),
            "神圣之力": SkillTreeNode("神圣之力", SkillType.MAGIC, 5, "神圣魔法进阶",
                                     level_descriptions={
                                         1: "神圣触媒：治疗+1",
                                         2: "神圣祝福：治疗+2",
                                         3: "神圣恩典：治疗+3，群体治疗",
                                         4: "神圣化身：治疗+4，复活",
                                         5: "神圣降临：治疗+5，终极治愈"
                                     }),
            "暗影秘术": SkillTreeNode("暗影秘术", SkillType.MAGIC, 5, "暗影魔法进阶",
                                     prerequisites=["元素掌控"],
                                     level_descriptions={
                                         1: "暗影亲和：暗影法术+1",
                                         2: "暗影掌控：暗影法术+2",
                                         3: "暗影支配：暗影法术+3，暗影步",
                                         4: "暗影大师：暗影法术+4，暗影分身",
                                         5: "暗影之巅：暗影法术+5，终极暗影"
                                     }),
        },
        "潜行系": {
            "潜行": SkillTreeNode("潜行", SkillType.STEALTH, 5, "潜行技巧进阶",
                                 level_descriptions={
                                     1: "隐蔽：潜行+1",
                                     2: "无声移动：潜行+2",
                                     3: "暗影潜行：潜行+3，暗影中隐形",
                                     4: "大师潜行：潜行+4，消失",
                                     5: "暗影舞者：潜行+5，隐身攻击"
                                 }),
            "开锁": SkillTreeNode("开锁", SkillType.STEALTH, 5, "开锁技巧进阶",
                                 level_descriptions={
                                     1: "基础开锁：开锁+1",
                                     2: "熟练开锁：开锁+2",
                                     3: "精通开锁：开锁+3，解除陷阱",
                                     4: "大师开锁：开锁+4，魔法锁",
                                     5: "万能钥匙：开锁+5，瞬间解锁"
                                 }),
        },
        "社交系": {
            "交涉": SkillTreeNode("交涉", SkillType.SOCIAL, 5, "社交技巧进阶",
                                 level_descriptions={
                                     1: "基础交涉：社交+1",
                                     2: "说服：社交+2",
                                     3: "精通交涉：社交+3，群体说服",
                                     4: "大师交涉：社交+4，魅惑",
                                     5: "外交大师：社交+5，终极说服"
                                 }),
            "威胁": SkillTreeNode("威胁", SkillType.SOCIAL, 5, "胁迫技巧进阶",
                                 prerequisites=["交涉"],
                                 level_descriptions={
                                     1: "基础威胁：恐吓+1",
                                     2: "恐吓：恐吓+2",
                                     3: "精通威胁：恐吓+3，震慑",
                                     4: "大师威胁：恐吓+4，屈服",
                                     5: "恐惧化身：恐吓+5，终极恐惧"
                                 }),
        },
        "生存系": {
            "野外生存": SkillTreeNode("野外生存", SkillType.SURVIVAL, 5, "野外生存进阶",
                                      level_descriptions={
                                          1: "自然感知：生存+1",
                                          2: "追踪：生存+2",
                                          3: "精通生存：生存+3，野外治愈",
                                          4: "大师生存：生存+4，动物沟通",
                                          5: "自然化身：生存+5，终极自然"
                                      }),
        }
    }

    def __init__(self):
        self.trees: Dict[str, Dict[str, SkillTreeNode]] = {}
        self.owned_skills: Dict[str, int] = {}  # skill_name → current_level
        self._init_default_trees()

    def _init_default_trees(self):
        """初始化默认技能树"""
        self.trees = {k: dict(v) for k, v in self.DEFAULT_TREES.items()}
        for tree in self.trees.values():
            for name, node in tree.items():
                self.owned_skills.setdefault(name, 0)

    def learn_skill(self, skill_name: str, player_level: int) -> Tuple[bool, str]:
        """学习新技能（1级）"""
        # 在所有树中查找技能
        for tree in self.trees.values():
            if skill_name in tree:
                node = tree[skill_name]
                ok, reason = node.can_advance_to(1, self.owned_skills, player_level)
                if ok:
                    self.owned_skills[skill_name] = 1
                    return True, f"学会了 {skill_name}"
                return False, reason
        return False, f"未找到技能: {skill_name}"

    def upgrade_skill(self, skill_name: str, player_level: int) -> Tuple[bool, str]:
        """升级技能"""
        if skill_name not in self.owned_skills:
            return False, "尚未学习该技能"

        current = self.owned_skills[skill_name]
        target_level = current + 1

        for tree in self.trees.values():
            if skill_name in tree:
                node = tree[skill_name]
                ok, reason = node.can_advance_to(target_level, self.owned_skills, player_level)
                if ok:
                    self.owned_skills[skill_name] = target_level
                    return True, f"{skill_name} 升级到 {target_level} 级"
                return False, reason
        return False, f"未找到技能: {skill_name}"

    def get_skill_bonus(self, skill_name: str) -> int:
        """获取技能当前等级加值"""
        level = self.owned_skills.get(skill_name, 0)
        return level

    def get_available_skills(self) -> List[str]:
        """获取所有可用技能列表"""
        skills = []
        for tree in self.trees.values():
            skills.extend(tree.keys())
        return skills

    def get_learned_skills(self) -> Dict[str, int]:
        """获取已学习的技能及其等级"""
        return {k: v for k, v in self.owned_skills.items() if v > 0}

    def get_upgradable_skills(self, player_level: int) -> List[Tuple[str, int, int]]:
        """获取可升级的技能列表：[(技能名, 当前等级, 目标等级)]"""
        upgradable = []
        for name, current_level in self.owned_skills.items():
            if current_level >= 5:
                continue  # 已达最高级
            for tree in self.trees.values():
                if name in tree:
                    node = tree[name]
                    target = current_level + 1
                    ok, _ = node.can_advance_to(target, self.owned_skills, player_level)
                    if ok:
                        upgradable.append((name, current_level, target))
                    break
        return upgradable


# ============================================================
# 3. 环境战斗系统 (匹配战斗规则补充.md)
# ============================================================

class EnvironmentSystem:
    """
    环境战斗系统：
    - 6种地形（高地/森林/室内/水域/狭窄通道/平原）
    - 4种天气（晴天/雨天/雪天/雾天）
    - 地形和天气对攻防、移动、远程的法术修正
    """

    def __init__(self):
        self.terrain = "平原"
        self.weather = "晴天"

    def set_terrain(self, terrain: str):
        """设置当前地形"""
        if terrain in config.TERRAIN_MODIFIERS:
            self.terrain = terrain

    def set_weather(self, weather: str):
        """设置当前天气"""
        if weather in config.WEATHER_MODIFIERS:
            self.weather = weather

    def get_terrain_modifier(self) -> Dict[str, Any]:
        """获取地形修正值"""
        return dict(config.TERRAIN_MODIFIERS.get(self.terrain, {}))

    def get_weather_modifier(self) -> Dict[str, Any]:
        """获取天气修正值"""
        return dict(config.WEATHER_MODIFIERS.get(self.weather, {}))

    def get_attack_modifier(self) -> int:
        """获取总攻击修正（地形+天气）"""
        terrain_mod = self.get_terrain_modifier().get("attack", 0)
        return terrain_mod

    def get_defense_modifier(self) -> int:
        """获取总防御修正（地形+天气）"""
        terrain_mod = self.get_terrain_modifier().get("defense", 0)
        return terrain_mod

    def get_ranged_modifier(self) -> int:
        """获取远程攻击修正"""
        t = self.get_terrain_modifier()
        w = self.get_weather_modifier()
        return t.get("ranged", 0) + w.get("ranged", 0)

    def get_spell_modifier(self, damage_type: str) -> int:
        """
        获取法术伤害修正
        如雨天→火系-2，水系+2；雪天→寒冷+2
        """
        weather_mods = self.get_weather_modifier()
        type_map = {
            "火焰": "fire", "火": "fire",
            "冷冻": "cold", "冰": "cold", "寒冷": "cold",
            "水系": "water", "水": "water",
        }
        mapped = type_map.get(damage_type, "")
        if mapped and mapped in weather_mods:
            return weather_mods[mapped]

        # 水域地形：火系增强+2
        if self.terrain == "水域" and damage_type in ("火焰", "火"):
            return 2

        return 0

    def get_move_penalty(self) -> int:
        """获取移动惩罚"""
        t = self.get_terrain_modifier()
        w = self.get_weather_modifier()
        return t.get("move", 0) + w.get("move", 0)

    def get_environment_description(self) -> str:
        """获取环境描述"""
        t = self.get_terrain_modifier()
        w = self.get_weather_modifier()
        parts = [f"地形: {self.terrain} ({t.get('description', '')})",
                 f"天气: {self.weather} ({w.get('description', '')})"]
        return " | ".join(parts)

    def random_environment(self):
        """随机设置地形和天气"""
        self.terrain = random.choice(list(config.TERRAIN_MODIFIERS.keys()))
        self.weather = random.choice(list(config.WEATHER_MODIFIERS.keys()))


# ============================================================
# 4. 团队组合技系统
# ============================================================

class TeamComboSystem:
    """
    团队组合技系统
    支持：双重打击、掩护射击、夹击战术、集体护盾、元素共鸣
    """

    def __init__(self):
        self.combos = dict(config.TEAM_COMBOS)

    def get_available_combos(self, ally_count: int) -> List[str]:
        """根据友方数量返回可用组合技"""
        available = []
        for name, combo in self.combos.items():
            if ally_count + 1 >= combo["min_players"]:
                available.append(name)
        return available

    def execute_combo(self, combo_name: str, participants: int,
                      base_damage: int = 0) -> Dict[str, Any]:
        """
        执行组合技
        participants: 参与人数
        base_damage: 基础伤害
        返回修正后的战斗效果
        """
        combo = self.combos.get(combo_name)
        if not combo:
            return {"error": f"未知组合技: {combo_name}"}

        result = {
            "combo": combo_name,
            "description": combo["description"],
            "damage_bonus": combo.get("damage_bonus", 0),
            "defense_bonus": combo.get("defense_bonus", 0),
            "total_damage": base_damage + combo.get("damage_bonus", 0),
            "attack_advantage": combo.get("attack_advantage", False),
            "target_disadvantage": combo.get("target_disadvantage", False),
            "spell_bonus": combo.get("spell_bonus", 0),
        }
        return result


# ============================================================
# 5. BOSS阶段系统 (三阶段)
# ============================================================

@dataclass
class BossPhase:
    """BOSS阶段"""
    phase_number: int                     # 阶段编号 1/2/3
    name: str                             # 阶段名称
    hp_remaining: int                     # 该阶段HP
    max_hp: int                           # 最大HP
    attack: int                           # 攻击力
    defense: int                          # 防御力
    abilities: List[str] = field(default_factory=list)  # 特殊能力
    is_environment_active: bool = False   # 是否改变战场环境
    environment_change: str = ""          # 环境变化描述


class BossFightSystem:
    """
    三阶段BOSS战斗系统
    每个BOSS经历：标准形态 → 能量形态 → 真身形态
    每个阶段有不同HP/攻击/防御和行为模式
    """

    def __init__(self):
        self.current_phase = 0
        self.phases: List[BossPhase] = []
        self.is_active = False

    def initialize_boss(self, boss_name: str, base_hp: int, base_attack: int,
                        base_defense: int) -> List[BossPhase]:
        """
        根据BOSS基础属性初始化三阶段
        base_hp: 基础HP，阶段间分配
        返回阶段列表
        """
        self.phases = []
        templates = config.BOSS_PHASE_TEMPLATES

        for i, (phase_key, template) in enumerate(templates.items()):
            phase_hp = int(base_hp * template["hp_multiplier"])
            phase_attack = int(base_attack * template["attack_multiplier"])
            phase_defense = int(base_defense * template["defense_multiplier"])

            # 阶段特殊能力
            abilities = list(template["abilities"])
            if i == 0:
                abilities.append("常规攻击模式")
            elif i == 1:
                abilities.append("元素攻击增强")
                abilities.append("获得特殊弱点")
            elif i == 2:
                abilities.append("终极技能激活")
                abilities.append("道德弱点暴露")

            phase = BossPhase(
                phase_number=i + 1,
                name=template["name"],
                hp_remaining=phase_hp,
                max_hp=phase_hp,
                attack=phase_attack,
                defense=phase_defense,
                abilities=abilities,
                is_environment_active=(i == 1),  # 第二阶段开始改变环境
                environment_change=f"{boss_name}进入了{template['name']}！{self._get_phase_environment_desc(i)}"
            )
            self.phases.append(phase)

        self.current_phase = 0
        self.is_active = True
        return self.phases

    def _get_phase_environment_desc(self, phase_index: int) -> str:
        """获取阶段环境变化描述"""
        descs = {
            0: "战场保持稳定。",
            1: "能量波动扭曲了战场，元素攻击变得更强，但对应抗性降低！",
            2: "BOSS释放了全部力量，环境变得极其危险，但道德弱点已经暴露！"
        }
        return descs.get(phase_index, "")

    def get_current_phase(self) -> Optional[BossPhase]:
        """获取当前阶段"""
        if 0 <= self.current_phase < len(self.phases):
            return self.phases[self.current_phase]
        return None

    def advance_phase(self) -> bool:
        """进入下一阶段，返回是否还有下一阶段"""
        if self.current_phase < len(self.phases) - 1:
            self.current_phase += 1
            return True
        self.is_active = False
        return False

    def take_damage(self, damage: int) -> Dict[str, Any]:
        """
        对当前阶段造成伤害
        返回：是否阶段结束、阶段变化、剩余HP
        """
        phase = self.get_current_phase()
        if not phase:
            return {"error": "无活跃阶段"}

        phase.hp_remaining -= damage
        result = {
            "damage": damage,
            "phase_hp_remaining": phase.hp_remaining,
            "phase_max_hp": phase.max_hp,
            "phase_number": phase.phase_number,
            "phase_name": phase.name,
            "phase_ended": phase.hp_remaining <= 0,
            "boss_defeated": False
        }

        if phase.hp_remaining <= 0:
            has_next = self.advance_phase()
            if not has_next:
                result["boss_defeated"] = True
                result["next_phase"] = None
            else:
                next_phase = self.get_current_phase()
                result["next_phase"] = {
                    "phase_number": next_phase.phase_number,
                    "name": next_phase.name,
                    "abilities": next_phase.abilities,
                    "environment_change": next_phase.environment_change
                }

        return result

    def get_boss_status(self) -> Dict[str, Any]:
        """获取BOSS战状态"""
        phase = self.get_current_phase()
        if not phase:
            return {"active": False}

        return {
            "active": self.is_active,
            "current_phase": self.current_phase + 1,
            "total_phases": len(self.phases),
            "phase_name": phase.name,
            "hp_remaining": phase.hp_remaining,
            "hp_max": phase.max_hp,
            "attack": phase.attack,
            "defense": phase.defense,
            "abilities": phase.abilities,
            "environment_change": phase.environment_change if phase.is_environment_active else ""
        }

    def apply_weakness(self, weakness_type: str) -> int:
        """
        应用弱点修正
        第3阶段暴露道德弱点，根据伤害类型有额外效果
        返回伤害修正值
        """
        if self.current_phase == 2:  # 真身形态
            weakness_bonus = {
                "光明": 3,
                "暗影": 3,
                "神圣": 4,
                "诅咒": 2,
            }
            return weakness_bonus.get(weakness_type, 0)
        return 0


# ============================================================
# 6. 装备套装效果
# ============================================================

class EquipmentSetSystem:
    """
    装备套装系统（战斗规则补充.md）
    光明套装（4件）：治疗+1 → 对抗暗影优势 → 神圣庇护
    暗影套装（4件）：视野增强 → 暗影隐身 → 暗影链接
    平衡套装（4件）：全属性+1 → 元素抗性+1 → 平衡守护
    """

    def __init__(self):
        self.set_configs = dict(config.EQUIPMENT_SETS)

    def get_equipment_set_name(self, equipment: Equipment) -> Optional[str]:
        """判断装备所属套装"""
        name = equipment.name
        for set_name in self.set_configs:
            if set_name in name:
                return set_name
        return None

    def get_active_set_bonuses(self, equipped_items: List[Equipment]) -> Dict[str, Any]:
        """
        根据已装备物品计算套装效果
        返回：{套装名: {件数, 激活的加成列表}}
        """
        # 统计各套装的件数
        set_counts: Dict[str, int] = {}
        for eq in equipped_items:
            set_name = self.get_equipment_set_name(eq)
            if set_name:
                set_counts[set_name] = set_counts.get(set_name, 0) + 1

        # 计算激活的加成
        active_bonuses: Dict[str, Any] = {}
        for set_name, count in set_counts.items():
            config_set = self.set_configs.get(set_name)
            if not config_set:
                continue

            bonuses = config_set.get("bonuses", {})
            active_bonuses[set_name] = {
                "pieces": count,
                "threshold": config_set["pieces"],
                "activated": {}
            }

            for threshold, bonus in sorted(bonuses.items()):
                if count >= threshold:
                    active_bonuses[set_name]["activated"][threshold] = bonus

        return active_bonuses

    def apply_set_bonus_to_attack(self, equipped_items: List[Equipment],
                                   base_attack: int) -> int:
        """应用套装加成到攻击值"""
        bonuses = self.get_active_set_bonuses(equipped_items)
        modifier = 0
        for set_data in bonuses.values():
            for threshold_data in set_data["activated"].values():
                if threshold_data.get("all_stats_plus_1"):
                    modifier += 1
        return base_attack + modifier

    def apply_set_bonus_to_defense(self, equipped_items: List[Equipment],
                                    base_defense: int) -> int:
        """应用套装加成到防御值"""
        bonuses = self.get_active_set_bonuses(equipped_items)
        modifier = 0
        for set_data in bonuses.values():
            for threshold_data in set_data["activated"].values():
                if threshold_data.get("all_stats_plus_1"):
                    modifier += 1
        return base_defense + modifier


# ============================================================
# 7. 法术协同系统
# ============================================================

class SpellSynergySystem:
    """
    法术协同系统
    不同元素组合产生特殊效果：
    火+水=蒸汽云(掩护)，火+风=火焰旋风(DOT)
    水+风=暴风雨(远程劣势)，地+水=泥潭(减速)
    光+暗=能量爆发(大量伤害)
    """

    def __init__(self):
        self.synergies = dict(config.SPELL_SYNERGIES)

    def check_synergy(self, element_a: str, element_b: str) -> Optional[Dict[str, Any]]:
        """检查两个元素是否有协同效果"""
        # 标准化元素名称
        norm_map = {
            "火焰": "火焰", "火": "火焰", "fire": "火焰",
            "冷冻": "冷冻", "冰冻": "冷冻", "cold": "冷冻", "冰": "冷冻",
            "风暴": "风暴", "wind": "风暴", "风": "风暴",
            "大地": "大地", "earth": "大地", "地": "大地",
            "光明": "光明", "light": "光明", "光": "光明",
            "暗影": "暗影", "shadow": "暗影", "暗": "暗影"
        }
        elem_a = norm_map.get(element_a, element_a)
        elem_b = norm_map.get(element_b, element_b)

        # 双向检查
        key = (elem_a, elem_b)
        rev_key = (elem_b, elem_a)

        if key in self.synergies:
            return dict(self.synergies[key])
        if rev_key in self.synergies:
            return dict(self.synergies[rev_key])

        return None

    def apply_synergy(self, spell_a: Spell, spell_b: Spell) -> Optional[Dict[str, Any]]:
        """应用两个法术的协同效果"""
        # 提取法术的伤害类型作为元素类型
        elem_a = self._get_spell_element(spell_a)
        elem_b = self._get_spell_element(spell_b)

        synergy = self.check_synergy(elem_a, elem_b)
        if not synergy:
            return None

        result = dict(synergy)
        result["spells_used"] = [spell_a.name, spell_b.name]
        result["synergy_name"] = synergy.get("name", "未知协同")

        # 计算协同伤害
        base_damage = 0
        try:
            if spell_a.damage_dice and 'd' in spell_a.damage_dice:
                dice_a = spell_a.damage_dice
                if dice_a.count('d') == 1:
                    count, die = dice_a.split('d')
                    base_damage += sum(random.randint(1, int(die)) for _ in range(int(count)))
            if spell_b.damage_dice and 'd' in spell_b.damage_dice:
                dice_b = spell_b.damage_dice
                if dice_b.count('d') == 1:
                    count, die = dice_b.split('d')
                    base_damage += sum(random.randint(1, int(die)) for _ in range(int(count)))
        except (ValueError, IndexError):
            base_damage = 5  # 默认协同伤害

        # 协同加成
        bonus_damage = synergy.get("damage_bonus", 0)
        dot_damage = synergy.get("dot_damage", "")
        result["total_damage"] = base_damage + bonus_damage
        result["dot"] = dot_damage

        return result

    def _get_spell_element(self, spell: Spell) -> str:
        """获取法术的元素类型"""
        type_map = {
            "火焰": "火焰", "火": "火焰", "火球": "火焰",
            "冷冻": "冷冻", "冰": "冷冻", "冰冻": "冷冻",
            "风暴": "风暴", "风": "风暴", "雷电": "风暴",
            "大地": "大地", "地": "大地", "土": "大地",
            "光明": "光明", "光": "光明", "圣光": "光明",
            "暗影": "暗影", "暗": "暗影", "黑暗": "暗影",
        }
        for key, elem in type_map.items():
            if key in spell.name or key in spell.damage_type or key in spell.school:
                return elem
        return spell.school  # fallback


# ============================================================
# 8. 持久化系统（存档/读档）
# ============================================================

class SaveLoadSystem:
    """
    存档/读档系统
    用JSON格式保存游戏状态
    支持最多9个存档位
    """

    def __init__(self):
        self.save_dir = config.SAVE_DIR
        os.makedirs(self.save_dir, exist_ok=True)

    def _get_save_path(self, slot: int) -> str:
        """获取存档文件路径"""
        return os.path.join(self.save_dir, f"save_{slot}{config.SAVE_FILE_EXTENSION}")

    def save_game(self, game_engine: Any, slot: int) -> Tuple[bool, str]:
        """
        保存游戏状态
        game_engine: GameEngine实例
        slot: 存档位 (1-9)
        """
        if not (1 <= slot <= config.MAX_SAVE_SLOTS):
            return False, f"存档位无效，请输入 1-{config.MAX_SAVE_SLOTS}"

        game = game_engine.game
        if not game.player:
            return False, "没有玩家角色可保存"

        try:
            save_data = {
                "version": "1.0",
                "timestamp": __import__('datetime').datetime.now().isoformat(),
                "player": {
                    "name": game.player.name,
                    "background": game.player.background,
                    "character_class": game.player.character_class,
                    "level": game.player.level,
                    "experience": game.player.experience,
                    "health": game.player.health,
                    "max_health": game.player.max_health,
                    "gold": game.player.gold,
                    "current_chapter": game.player.current_chapter,
                    "inventory": game.player.inventory,
                    "completed_quests": game.player.completed_quests,
                    "progress": game.player.progress,
                    "attributes": {
                        "strength": game.player.attributes.strength,
                        "dexterity": game.player.attributes.dexterity,
                        "constitution": game.player.attributes.constitution,
                        "intelligence": game.player.attributes.intelligence,
                        "wisdom": game.player.attributes.wisdom,
                        "charisma": game.player.attributes.charisma
                    },
                    "morality": {
                        "light": game.player.morality.light,
                        "shadow": game.player.morality.shadow,
                        "balance": game.player.morality.balance
                    },
                    "skills": [{"name": s.name, "skill_type": s.skill_type.value,
                                "level": s.level, "description": s.description}
                               for s in game.player.skills],
                    "equipment_names": [eq.name for eq in game.player.equipment],
                    "spell_names": [sp.name for sp in game.player.spells]
                }
            }

            path = self._get_save_path(slot)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)

            return True, f"游戏已保存到存档位 {slot}"

        except Exception as e:
            return False, f"保存失败: {e}"

    def load_game(self, game_engine: Any, slot: int) -> Tuple[bool, str]:
        """
        加载游戏存档
        """
        if not (1 <= slot <= config.MAX_SAVE_SLOTS):
            return False, f"存档位无效，请输入 1-{config.MAX_SAVE_SLOTS}"

        path = self._get_save_path(slot)
        if not os.path.exists(path):
            return False, f"存档位 {slot} 不存在"

        try:
            with open(path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            pd = save_data["player"]

            # 创建玩家角色
            game_engine.create_character(pd["name"], pd["background"], pd["character_class"])
            player = game_engine.game.player

            # 恢复状态
            player.level = pd["level"]
            player.experience = pd["experience"]
            player.health = pd["health"]
            player.max_health = pd["max_health"]
            player.gold = pd["gold"]
            player.current_chapter = pd["current_chapter"]
            player.inventory = pd["inventory"]
            player.completed_quests = pd["completed_quests"]
            player.progress = pd["progress"]

            # 恢复属性
            attrs = pd["attributes"]
            player.attributes.strength = attrs["strength"]
            player.attributes.dexterity = attrs["dexterity"]
            player.attributes.constitution = attrs["constitution"]
            player.attributes.intelligence = attrs["intelligence"]
            player.attributes.wisdom = attrs["wisdom"]
            player.attributes.charisma = attrs["charisma"]

            # 恢复道德值
            mor = pd["morality"]
            player.morality.light = mor["light"]
            player.morality.shadow = mor["shadow"]
            player.morality.balance = mor["balance"]

            # 设置当前章节
            game_engine.game.current_chapter = game_engine.game.chapters[
                min(pd["current_chapter"] - 1, len(game_engine.game.chapters) - 1)
            ]

            return True, f"已从存档位 {slot} 加载游戏"

        except Exception as e:
            return False, f"读档失败: {e}"

    def list_saves(self) -> List[Dict[str, Any]]:
        """列出所有存档"""
        saves = []
        for slot in range(1, config.MAX_SAVE_SLOTS + 1):
            path = self._get_save_path(slot)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    saves.append({
                        "slot": slot,
                        "timestamp": data.get("timestamp", "未知"),
                        "player_name": data.get("player", {}).get("name", "未知"),
                        "level": data.get("player", {}).get("level", 0),
                        "chapter": data.get("player", {}).get("current_chapter", 0),
                    })
                except Exception:
                    saves.append({"slot": slot, "timestamp": "损坏", "player_name": "损坏的存档"})
        return saves

    def delete_save(self, slot: int) -> Tuple[bool, str]:
        """删除存档"""
        path = self._get_save_path(slot)
        if os.path.exists(path):
            os.remove(path)
            return True, f"已删除存档位 {slot}"
        return False, f"存档位 {slot} 不存在"


# ============================================================
# 9. NPC关系系统（集成到核心引擎）
# ============================================================

class NPCRelationshipSystem:
    """
    NPC关系系统
    集成gm_tools中的NPCRelationship到核心引擎
    关系值影响：对话选项、任务获取、战斗支援、装备价格
    """

    def __init__(self):
        self.relationships: Dict[str, int] = {}  # npc_name → relationship_score (-10 ~ 10)

    def initialize_npcs(self, npcs: List[NPC]):
        """初始化NPC关系"""
        for npc in npcs:
            if npc.name not in self.relationships:
                self.relationships[npc.name] = npc.relationship

    def update_relationship(self, npc_name: str, change: int):
        """更新与NPC的关系"""
        current = self.relationships.get(npc_name, 0)
        self.relationships[npc_name] = max(-10, min(10, current + change))

    def get_relationship(self, npc_name: str) -> int:
        """获取与NPC的关系值"""
        return self.relationships.get(npc_name, 0)

    def get_relationship_tier(self, npc_name: str) -> str:
        """获取关系等级描述"""
        score = self.get_relationship(npc_name)
        if score >= 8:
            return "极度友好"
        elif score >= 5:
            return "友好"
        elif score >= 1:
            return "中立-友好"
        elif score >= -2:
            return "中立"
        elif score >= -5:
            return "不友好"
        elif score >= -8:
            return "敌对"
        else:
            return "极度敌对"

    def is_quest_available(self, npc_name: str, required_relationship: int = 0) -> bool:
        """检查是否满足任务所需关系"""
        return self.get_relationship(npc_name) >= required_relationship

    def get_price_modifier(self, npc_name: str) -> float:
        """根据关系返回价格修正（1.0 = 标准）"""
        score = self.get_relationship(npc_name)
        if score >= 8:
            return 0.7   # 7折
        elif score >= 5:
            return 0.85  # 8.5折
        elif score >= 0:
            return 1.0   # 标准
        elif score >= -3:
            return 1.15  # +15%
        else:
            return 1.3   # +30%

    def get_all_relationships(self) -> Dict[str, Dict[str, Any]]:
        """获取所有NPC关系状态"""
        result = {}
        for name, score in self.relationships.items():
            result[name] = {
                "score": score,
                "tier": self.get_relationship_tier(name),
                "price_modifier": self.get_price_modifier(name)
            }
        return result
