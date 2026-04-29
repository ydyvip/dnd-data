"""
《暗影王座的救赎》GM工具包
提供GM工具、数据管理和游戏管理功能
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog


class GMToolType(Enum):
    """GM工具类型"""
    NPC_TRACKER = "NPC关系追踪"
    COMBAT_CALCULATOR = "战斗难度计算器"
    MORALITY_TRACKER = "道德值追踪"
    RANDOM_EVENTS = "随机事件表"
    QUICK_ENCOUNTER = "快速遭遇生成器"
    PLOT_GENERATOR = "急救剧情生成器"
    WORLD_BUILDER = "世界构建工具"
    LOOT_GENERATOR = "战利品生成器"


@dataclass
class NPCRelationship:
    """NPC关系数据"""
    npc_name: str
    relationship_score: int  # -10 到 10
    relationship_type: str  # 友好、中立、敌对
    last_interaction: str
    quests_completed: List[str] = field(default_factory=list)
    gifts_received: List[str] = field(default_factory=list)
    favors_asked: List[str] = field(default_factory=list)


@dataclass
class CombatScenario:
    """战斗场景"""
    name: str
    difficulty: str  # 简单、普通、困难、极难
    monsters: List[str]
    terrain: str
    weather: str
    objectives: List[str]
    rewards: List[str]


@dataclass
class RandomEvent:
    """随机事件"""
    name: str
    trigger: str
    description: str
    outcomes: List[str]
    morality_impact: Dict[str, int]
    experience_reward: int


@dataclass
class QuestTemplate:
    """任务模板"""
    name: str
    description: str
    chapter: int
    requirements: Dict[str, int]
    rewards: Dict[str, int]
    morality_impact: Dict[str, int]
    difficulty: str
    time_limit: Optional[int] = None


class GMTracker:
    """GM追踪器"""
    
    def __init__(self):
        self.npc_relationships: Dict[str, NPCRelationship] = {}
        self.player_progress: Dict[str, Any] = {}
        self.current_chapter: int = 1
        self.game_session_start = datetime.now()
        self.session_notes: List[str] = []
        
    def add_npc_relationship(self, npc_name: str, initial_score: int = 0):
        """添加NPC关系"""
        self.npc_relationships[npc_name] = NPCRelationship(
            npc_name=npc_name,
            relationship_score=initial_score,
            relationship_type="中立" if initial_score == 0 else "友好" if initial_score > 0 else "敌对",
            last_interaction="初次见面"
        )
    
    def update_npc_relationship(self, npc_name: str, change: int, interaction_type: str):
        """更新NPC关系"""
        if npc_name in self.npc_relationships:
            relationship = self.npc_relationships[npc_name]
            relationship.relationship_score = max(-10, min(10, relationship.relationship_score + change))
            
            # 更新关系类型
            if relationship.relationship_score > 5:
                relationship.relationship_type = "非常友好"
            elif relationship.relationship_score > 0:
                relationship.relationship_type = "友好"
            elif relationship.relationship_score > -5:
                relationship.relationship_type = "中立"
            else:
                relationship.relationship_type = "敌对"
            
            relationship.last_interaction = interaction_type
            return True
        return False
    
    def get_npc_relationship(self, npc_name: str) -> Optional[NPCRelationship]:
        """获取NPC关系"""
        return self.npc_relationships.get(npc_name)
    
    def add_session_note(self, note: str):
        """添加游戏笔记"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.session_notes.append(f"[{timestamp}] {note}")
    
    def get_session_notes(self) -> List[str]:
        """获取游戏笔记"""
        return self.session_notes.copy()


class CombatCalculator:
    """战斗难度计算器"""
    
    def __init__(self):
        self.monster_difficulty_ratings = {
            "哥布林": 1,
            "骷髅战士": 2,
            "暗影生物": 3,
            "元素精魄": 4,
            "古代守护者": 5,
            "暗影君主": 20
        }
    
    def calculate_difficulty(self, player_level: int, monster_names: List[str], 
                           player_count: int = 1) -> str:
        """计算战斗难度"""
        total_difficulty = 0
        
        for monster_name in monster_names:
            difficulty = self.monster_difficulty_ratings.get(monster_name, 1)
            total_difficulty += difficulty
        
        # 调整玩家数量影响
        total_difficulty = total_difficulty / player_count
        
        # 确定难度等级
        if total_difficulty <= player_level * 0.5:
            return "简单"
        elif total_difficulty <= player_level:
            return "普通"
        elif total_difficulty <= player_level * 1.5:
            return "困难"
        else:
            return "极难"
    
    def generate_balanced_encounter(self, player_level: int, player_count: int = 1) -> List[str]:
        """生成平衡的遭遇"""
        difficulty = self.calculate_difficulty(player_level, [], player_count)
        
        # 根据难度选择怪物
        if difficulty == "简单":
            monsters = ["哥布林"] * random.randint(2, 4)
        elif difficulty == "普通":
            monsters = random.sample(["哥布林", "骷髅战士"], k=random.randint(2, 3))
        elif difficulty == "困难":
            monsters = random.sample(["骷髅战士", "暗影生物"], k=random.randint(2, 3))
        else:  # 极难
            monsters = ["暗影君主"] if player_level >= 15 else ["元素精魄", "暗影生物"]
        
        return monsters


class WorldBuilder:
    """世界构建工具"""
    
    def __init__(self):
        self.locations = {}
        self.factions = {}
        self.world_history = []
        self.current_events = []
    
    def create_location(self, name: str, description: str, faction_influence: Dict[str, int]):
        """创建地点"""
        self.locations[name] = {
            "description": description,
            "faction_influence": faction_influence,
            "important_places": [],
            "secrets": [],
            "connections": []
        }
    
    def create_faction(self, name: str, description: str, goal: str, enemies: List[str]):
        """创建势力"""
        self.factions[name] = {
            "description": description,
            "goal": goal,
            "enemies": enemies,
            "allies": [],
            "territory": [],
            "leader": "",
            "resources": []
        }
    
    def add_world_event(self, event: str, date: str, importance: str):
        """添加世界事件"""
        self.world_history.append({
            "event": event,
            "date": date,
            "importance": importance,
            "consequences": []
        })
    
    def generate_random_location(self) -> Dict[str, str]:
        """生成随机地点"""
        location_templates = [
            {
                "name": "古老神庙",
                "description": "一座被遗忘的神庙，里面充满了神秘的力量和危险的守护者。",
                "secrets": ["古代预言", "隐藏宝藏", "邪恶仪式"]
            },
            {
                "name": "精灵村庄",
                "description": "建在古老树上的精灵村庄，与自然和谐共生。",
                "secrets": ["自然魔法", "精灵历史", "森林秘密"]
            },
            {
                "name": "地下城",
                "description": "深入地下的复杂迷宫，充满了陷阱和怪物。",
                "secrets": ["古代实验室", "魔法物品", "迷失的王国"]
            },
            {
                "name": "商业城镇",
                "description": "繁华的商业中心，来自各地的商人和冒险者聚集于此。",
                "secrets": ["走私网络", "政治阴谋", "黑市交易"]
            }
        ]
        
        return random.choice(location_templates)


class LootGenerator:
    """战利品生成器"""
    
    def __init__(self):
        self.loot_tables = {
            "common": [
                {"name": "金币", "value": random.randint(10, 100), "rarity": "common"},
                {"name": "治疗药水", "value": 50, "rarity": "common", "effect": "恢复2d8生命值"},
                {"name": "魔法武器", "value": random.randint(100, 500), "rarity": "uncommon"},
                {"name": "防具", "value": random.randint(50, 300), "rarity": "common"}
            ],
            "uncommon": [
                {"name": "魔法戒指", "value": random.randint(300, 800), "rarity": "rare"},
                {"name": "魔法斗篷", "value": random.randint(400, 1000), "rarity": "rare"},
                {"name": "药水组合", "value": random.randint(200, 500), "rarity": "uncommon"}
            ],
            "rare": [
                {"name": "传说武器", "value": random.randint(1000, 5000), "rarity": "legendary"},
                {"name": "神器", "value": random.randint(5000, 20000), "rarity": "legendary"},
                {"name": "魔法书", "value": random.randint(800, 3000), "rarity": "rare"}
            ]
        }
    
    def generate_loot(self, difficulty: str) -> List[Dict[str, Any]]:
        """根据难度生成战利品"""
        if difficulty == "简单":
            table = self.loot_tables["common"]
        elif difficulty == "普通":
            table = random.choice([self.loot_tables["common"], self.loot_tables["uncommon"]])
        elif difficulty == "困难":
            table = random.choice([self.loot_tables["uncommon"], self.loot_tables["rare"]])
        else:  # 极难
            table = self.loot_tables["rare"]
        
        # 生成多个战利品
        loot_count = random.randint(1, 3)
        loot = []
        for _ in range(loot_count):
            item = random.choice(table)
            loot.append(item.copy())
        
        return loot
    
    def generate_magic_item(self) -> Dict[str, Any]:
        """生成魔法物品"""
        item_types = [
            {"name": "魔法剑", "effect": "攻击+2", "value": 500},
            {"name": "魔法盾", "effect": "防御+2", "value": 400},
            {"name": "魔法戒指", "effect": "所有豁免+1", "value": 800},
            {"name": "魔法斗篷", "effect": "隐蔽+2", "value": 600},
            {"name": "魔法项链", "effect": "生命值+20", "value": 700},
            {"name": "魔法靴子", "effect": "移动速度+10尺", "value": 300}
        ]
        
        return random.choice(item_types)


class PlotGenerator:
    """急救剧情生成器"""
    
    def __init__(self):
        self.plot_templates = [
            {
                "name": "神秘失踪",
                "setup": "村庄里的孩子神秘失踪了",
                "twist": "实际上是被邪恶法师绑架用于黑暗仪式",
                "resolution": "玩家需要找到并拯救孩子们，阻止仪式的完成"
            },
            {
                "name": "瘟疫蔓延",
                "setup": "奇怪的瘟疫在村庄里蔓延",
                "twist": "瘟疫是由某个NPC故意散布的",
                "resolution": "找出真正的元凶并找到解药"
            },
            {
                "name": "古代预言",
                "setup": "发现了关于暗影王座的古老预言",
                "twist": "预言中的英雄实际上可能是暗影君主的转世",
                "resolution": "玩家需要重新解释预言，找到真正的拯救之道"
            },
            {
                "name": "背叛之谜",
                "setup": "盟友突然背叛了玩家",
                "twist": "背叛是被迫的，被黑魔法控制",
                "resolution": "解除控制，恢复信任，找到真正的敌人"
            },
            {
                "name": "时空异常",
                "setup": "时空开始扭曲，出现不同时代的场景",
                "twist": "这是暗影君主的时间魔法实验",
                "resolution": "破坏时间装置，修复时空裂缝"
            }
        ]
    
    def generate_plot(self) -> Dict[str, str]:
        """生成随机剧情"""
        return random.choice(self.plot_templates)
    
    def generate_custom_plot(self, theme: str, tone: str) -> Dict[str, str]:
        """根据主题和语调生成自定义剧情"""
        # 这里可以根据主题和语调进行更复杂的生成逻辑
        base_plot = self.generate_plot()
        
        # 根据主题调整
        if theme == "爱情":
            base_plot["setup"] = base_plot["setup"].replace("村庄", "情侣")
            base_plot["twist"] = base_plot["twist"].replace("邪恶法师", "嫉妒的情敌")
        
        elif theme == "政治":
            base_plot["setup"] = base_plot["setup"].replace("村庄", "王城")
            base_plot["twist"] = base_plot["twist"].replace("邪恶法师", "叛国贵族")
        
        elif theme == "恐怖":
            base_plot["setup"] = base_plot["setup"].replace("奇怪", "令人恐惧")
            base_plot["twist"] = base_plot["twist"].replace("黑暗仪式", "血腥献祭")
        
        return base_plot


class GMToolManager:
    """GM工具管理器"""
    
    def __init__(self):
        self.tracker = GMTracker()
        self.combat_calculator = CombatCalculator()
        self.world_builder = WorldBuilder()
        self.loot_generator = LootGenerator()
        self.plot_generator = PlotGenerator()
        self.random_events = self.generate_random_events()
        
    def generate_random_events(self) -> List[RandomEvent]:
        """生成随机事件列表"""
        return [
            RandomEvent(
                "神秘的旅人",
                "在路上遇到受伤的旅人",
                "一个受伤的旅人请求帮助，他声称被强盗袭击",
                ["帮助他，获得信息", "无视他，继续前进", "抢劫他"],
                {"light": 2, "shadow": -1, "balance": 0},
                50
            ),
            RandomEvent(
                "古代遗迹发现",
                "探索时发现隐藏的遗迹",
                "在森林深处发现了一座被遗忘的古代遗迹",
                ["探索遗迹，寻找宝藏", "标记位置，稍后返回", "警告他人，避免危险"],
                {"light": 1, "shadow": 1, "balance": 1},
                100
            ),
            RandomEvent(
                "村庄庆典",
                "进入正在举办庆典的村庄",
                "村庄正在举办丰收庆典，邀请玩家参加",
                ["参加庆典，获得好感", "帮忙准备，获得报酬", "悄悄离开，避免麻烦"],
                {"light": 1, "balance": 2, "shadow": -1},
                30
            ),
            RandomEvent(
                "魔法异常",
                "周围的魔法开始异常",
                "突然感觉到周围的魔法场变得不稳定",
                ["研究异常，寻找原因", "尽快离开异常区域", "利用异常，获得力量"],
                {"light": -1, "shadow": 2, "balance": 0},
                75
            ),
            RandomEvent(
                "神秘商人",
                "遇到神秘的旅行商人",
                "一个神秘的商人贩卖着奇怪的物品",
                ["购买物品", "询问物品来历", "离开不买"],
                {"light": 0, "shadow": 1, "balance": 1},
                25
            )
        ]
    
    def get_random_event(self) -> RandomEvent:
        """获取随机事件"""
        return random.choice(self.random_events)
    
    def generate_quest_template(self, difficulty: str) -> QuestTemplate:
        """生成任务模板"""
        quest_templates = {
            "简单": {
                "name": "收集草药",
                "description": "村庄的药剂师需要一些特定的草药来制作药剂",
                "requirements": {"herbs": 5},
                "rewards": {"experience": 100, "gold": 50},
                "morality_impact": {"light": 1, "shadow": 0, "balance": 0}
            },
            "普通": {
                "name": "清理强盗",
                "description": "附近的强盗营地威胁着村庄的安全",
                "requirements": {"robbers_defeated": 3},
                "rewards": {"experience": 200, "gold": 100},
                "morality_impact": {"light": 2, "shadow": -1, "balance": 0}
            },
            "困难": {
                "name": "探索古代遗迹",
                "description": "传说中的古代遗迹中可能藏着重要的信息",
                "requirements": {"relored_explored": 1, "artifacts_found": 2},
                "rewards": {"experience": 500, "gold": 200},
                "morality_impact": {"light": 1, "shadow": 1, "balance": 1}
            }
        }
        
        template = quest_templates[difficulty].copy()
        return QuestTemplate(
            name=template["name"],
            description=template["description"],
            chapter=1,  # 默认章节
            requirements=template["requirements"],
            rewards=template["rewards"],
            morality_impact=template["morality_impact"],
            difficulty=difficulty
        )
    
    def create_session_summary(self) -> str:
        """创建游戏会话总结"""
        summary = f"""
=== 游戏会话总结 ===
开始时间: {self.tracker.game_session_start}
结束时间: {datetime.now()}
持续时间: {datetime.now() - self.tracker.game_session_start}

=== 当前进度 ===
章节: {self.tracker.current_chapter}
NPC关系: {len(self.tracker.npc_relationships)}
已完成任务: {len([note for note in self.tracker.session_notes if '任务完成' in note])}

=== 游戏笔记 ===
"""
        for note in self.tracker.session_notes:
            summary += f"- {note}\n"
        
        return summary


# GM工具GUI界面
class GMToolsGUI:
    """GM工具GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("GM工具包")
        self.root.geometry("800x600")
        
        # 初始化GM工具管理器
        self.gm_manager = GMToolManager()
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面元素"""
        # 标题
        title_label = tk.Label(self.root, text="GM工具包", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 工具按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # NPC关系追踪按钮
        npc_button = tk.Button(button_frame, text="NPC关系追踪", 
                              command=self.show_npc_tracker,
                              bg="#4CAF50", fg="white", font=("Arial", 10))
        npc_button.grid(row=0, column=0, padx=5, pady=5)
        
        # 战斗难度计算器按钮
        combat_button = tk.Button(button_frame, text="战斗难度计算器", 
                                 command=self.show_combat_calculator,
                                 bg="#2196F3", fg="white", font=("Arial", 10))
        combat_button.grid(row=0, column=1, padx=5, pady=5)
        
        # 随机事件按钮
        events_button = tk.Button(button_frame, text="随机事件表", 
                                 command=self.show_random_events,
                                 bg="#ff9800", fg="white", font=("Arial", 10))
        events_button.grid(row=1, column=0, padx=5, pady=5)
        
        # 剧情生成器按钮
        plot_button = tk.Button(button_frame, text="急救剧情生成器", 
                               command=self.show_plot_generator,
                               bg="#9c27b0", fg="white", font=("Arial", 10))
        plot_button.grid(row=1, column=1, padx=5, pady=5)
        
        # 战利品生成器按钮
        loot_button = tk.Button(button_frame, text="战利品生成器", 
                               command=self.show_loot_generator,
                               bg="#f44336", fg="white", font=("Arial", 10))
        loot_button.grid(row=2, column=0, padx=5, pady=5)
        
        # 世界构建工具按钮
        world_button = tk.Button(button_frame, text="世界构建工具", 
                                command=self.show_world_builder,
                                bg="#607d8b", fg="white", font=("Arial", 10))
        world_button.grid(row=2, column=1, padx=5, pady=5)
        
        # 信息显示区域
        self.info_frame = tk.LabelFrame(self.root, text="信息显示", font=("Arial", 12, "bold"))
        self.info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=15, font=("Arial", 10))
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 初始化信息
        self.info_text.insert(tk.END, "欢迎使用GM工具包！\n\n")
        self.info_text.insert(tk.END, "选择上方的工具来开始使用各种GM功能。\n\n")
        self.info_text.insert(tk.END, "功能说明：\n")
        self.info_text.insert(tk.END, "- NPC关系追踪：管理和追踪NPC与玩家的关系\n")
        self.info_text.insert(tk.END, "- 战斗难度计算器：计算战斗的平衡性\n")
        self.info_text.insert(tk.END, "- 随机事件表：生成即兴游戏事件\n")
        self.info_text.insert(tk.END, "- 急救剧情生成器：生成紧急剧情线\n")
        self.info_text.insert(tk.END, "- 战利品生成器：生成游戏战利品\n")
        self.info_text.insert(tk.END, "- 世界构建工具：构建游戏世界观\n")
    
    def show_npc_tracker(self):
        """显示NPC关系追踪器"""
        tracker_window = tk.Toplevel(self.root)
        tracker_window.title("NPC关系追踪器")
        tracker_window.geometry("600x400")
        
        # 添加NPC区域
        add_frame = tk.Frame(tracker_window)
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="NPC名称:").pack(side="left")
        npc_name_entry = tk.Entry(add_frame)
        npc_name_entry.pack(side="left", padx=5)
        
        def add_npc():
            name = npc_name_entry.get()
            if name:
                self.gm_manager.tracker.add_npc_relationship(name)
                npc_name_entry.delete(0, tk.END)
                messagebox.showinfo("成功", f"已添加NPC: {name}")
        
        tk.Button(add_frame, text="添加NPC", command=add_npc).pack(side="left")
        
        # 关系显示区域
        display_frame = tk.Frame(tracker_window)
        display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建树形显示
        tree = ttk.Treeview(display_frame, columns=("关系", "最后互动"), show="tree headings")
        tree.heading("#0", text="NPC")
        tree.heading("关系", text="关系值")
        tree.heading("最后互动", text="最后互动")
        tree.column("#0", width=150)
        tree.column("关系", width=100)
        tree.column("最后互动", width=200)
        tree.pack(fill="both", expand=True)
        
        # 刷新显示
        def refresh_display():
            tree.delete(*tree.get_children())
            for npc_name, relationship in self.gm_manager.tracker.npc_relationships.items():
                tree.insert("", "end", text=npc_name, 
                           values=(f"{relationship.relationship_score} ({relationship.relationship_type})", 
                                  relationship.last_interaction))
        
        refresh_display()
        
        # 操作按钮
        button_frame = tk.Frame(tracker_window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="刷新", command=refresh_display).pack(side="left", padx=5)
        tk.Button(button_frame, text="添加笔记", command=self.add_session_note).pack(side="left", padx=5)
    
    def show_combat_calculator(self):
        """显示战斗难度计算器"""
        calc_window = tk.Toplevel(self.root)
        calc_window.title("战斗难度计算器")
        calc_window.geometry("500x300")
        
        # 输入区域
        input_frame = tk.Frame(calc_window)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="玩家等级:").grid(row=0, column=0, padx=5)
        level_entry = tk.Entry(input_frame)
        level_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="玩家数量:").grid(row=1, column=0, padx=5)
        count_entry = tk.Entry(input_frame)
        count_entry.grid(row=1, column=1, padx=5)
        
        tk.Label(input_frame, text="怪物数量:").grid(row=2, column=0, padx=5)
        monster_count_entry = tk.Entry(input_frame)
        monster_count_entry.grid(row=2, column=1, padx=5)
        
        tk.Label(input_frame, text="怪物类型:").grid(row=3, column=0, padx=5)
        monster_type_combo = ttk.Combobox(input_frame, 
                                         values=["哥布林", "骷髅战士", "暗影生物", "元素精魄", "古代守护者"])
        monster_type_combo.grid(row=3, column=1, padx=5)
        
        # 结果显示
        result_label = tk.Label(calc_window, text="", font=("Arial", 12))
        result_label.pack(pady=10)
        
        # 计算按钮
        def calculate_difficulty():
            try:
                level = int(level_entry.get())
                count = int(count_entry.get())
                monster_count = int(monster_count_entry.get())
                monster_type = monster_type_combo.get()
                
                monsters = [monster_type] * monster_count
                difficulty = self.gm_manager.combat_calculator.calculate_difficulty(level, monsters, count)
                
                result_label.config(text=f"战斗难度: {difficulty}")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字！")
        
        tk.Button(calc_window, text="计算难度", command=calculate_difficulty).pack(pady=10)
    
    def show_random_events(self):
        """显示随机事件表"""
        events_window = tk.Toplevel(self.root)
        events_window.title("随机事件表")
        events_window.geometry("600x400")
        
        # 事件显示区域
        text_area = scrolledtext.ScrolledText(events_window, height=20, font=("Arial", 10))
        text_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 生成并显示随机事件
        event = self.gm_manager.get_random_event()
        
        event_text = f"""
=== 随机事件: {event.name} ===

触发条件: {event.trigger}

描述: {event.description}

可能结果:
"""
        for outcome in event.outcomes:
            event_text += f"- {outcome}\n"
        
        event_text += f"\n道德影响: {event.morality_impact}\n"
        event_text += f"经验奖励: {event.experience_reward}点\n"
        
        text_area.insert(tk.END, event_text)
        
        # 生成新事件按钮
        tk.Button(events_window, text="生成新事件", 
                 command=lambda: self.refresh_random_events(events_window, text_area)).pack(pady=5)
    
    def refresh_random_events(self, window, text_area):
        """刷新随机事件"""
        text_area.delete(1.0, tk.END)
        event = self.gm_manager.get_random_event()
        
        event_text = f"""
=== 随机事件: {event.name} ===

触发条件: {event.trigger}

描述: {event.description}

可能结果:
"""
        for outcome in event.outcomes:
            event_text += f"- {outcome}\n"
        
        event_text += f"\n道德影响: {event.morality_impact}\n"
        event_text += f"经验奖励: {event.experience_reward}点\n"
        
        text_area.insert(tk.END, event_text)
    
    def show_plot_generator(self):
        """显示剧情生成器"""
        plot_window = tk.Toplevel(self.root)
        plot_window.title("急救剧情生成器")
        plot_window.geometry("600x400")
        
        # 生成按钮
        tk.Button(plot_window, text="生成剧情", 
                 command=lambda: self.generate_plot_display(plot_window)).pack(pady=10)
        
        # 剧情显示区域
        self.plot_text = scrolledtext.ScrolledText(plot_window, height=15, font=("Arial", 10))
        self.plot_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def generate_plot_display(self, window):
        """生成并显示剧情"""
        plot = self.gm_manager.plot_generator.generate_plot()
        
        plot_text = f"""
=== 剧情模板: {plot['name']} ===

 setup: {plot['setup']}
 twist: {plot['twist']}
 resolution: {plot['resolution']}
"""
        self.plot_text.delete(1.0, tk.END)
        self.plot_text.insert(tk.END, plot_text)
    
    def show_loot_generator(self):
        """显示战利品生成器"""
        loot_window = tk.Toplevel(self.root)
        loot_window.title("战利品生成器")
        loot_window.geometry("500x300")
        
        # 输入区域
        tk.Label(loot_window, text="难度等级:").pack(pady=5)
        difficulty_combo = ttk.Combobox(loot_window, 
                                       values=["简单", "普通", "困难", "极难"])
        difficulty_combo.pack(pady=5)
        
        # 结果显示区域
        loot_text = scrolledtext.ScrolledText(loot_window, height=10, font=("Arial", 10))
        loot_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 生成按钮
        def generate_loot():
            difficulty = difficulty_combo.get()
            if difficulty:
                loot_list = self.gm_manager.loot_generator.generate_loot(difficulty)
                
                loot_result = f"=== {difficulty}难度战利品 ===\n\n"
                for item in loot_list:
                    loot_result += f"- {item['name']} (价值: {item['value']}金币)\n"
                
                # 随机生成一个魔法物品
                magic_item = self.gm_manager.loot_generator.generate_magic_item()
                loot_result += f"\n=== 魔法物品 ===\n"
                loot_result += f"- {magic_item['name']} (效果: {magic_item['effect']}, 价值: {magic_item['value']}金币)\n"
                
                loot_text.delete(1.0, tk.END)
                loot_text.insert(tk.END, loot_result)
        
        tk.Button(loot_window, text="生成战利品", command=generate_loot).pack(pady=5)
    
    def show_world_builder(self):
        """显示世界构建工具"""
        world_window = tk.Toplevel(self.root)
        world_window.title("世界构建工具")
        world_window.geometry("600x400")
        
        # 生成按钮
        tk.Button(world_window, text="生成随机地点", 
                 command=lambda: self.generate_random_location(world_window)).pack(pady=10)
        
        # 结果显示区域
        self.world_text = scrolledtext.ScrolledText(world_window, height=15, font=("Arial", 10))
        self.world_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def generate_random_location(self, window):
        """生成随机地点"""
        location = self.gm_manager.world_builder.generate_random_location()
        
        world_text = f"""
=== 随机地点生成 ===

地点名称: {location['name']}
描述: {location['description']}
秘密: {', '.join(location['secrets'])}
"""
        self.world_text.delete(1.0, tk.END)
        self.world_text.insert(tk.END, world_text)
    
    def add_session_note(self):
        """添加游戏笔记"""
        note = simpledialog.askstring("游戏笔记", "请输入笔记内容:")
        if note:
            self.gm_manager.tracker.add_session_note(note)
            messagebox.showinfo("成功", "笔记已添加！")


# 主程序
if __name__ == "__main__":
   
    root = tk.Tk()
    app = GMToolsGUI(root)
    root.mainloop()