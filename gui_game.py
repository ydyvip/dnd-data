"""
《暗影王座的救赎》DND游戏 - 图形用户界面版本
使用Tkinter创建的完整GUI游戏
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from shadow_throne_redemption import GameEngine


class CharacterCreationWindow:
    """角色创建窗口"""
    
    def __init__(self, parent, game_engine):
        self.parent = parent
        self.game_engine = game_engine
        self.window = tk.Toplevel(parent)
        self.window.title("角色创建")
        self.window.geometry("600x500")
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面元素"""
        # 角色名称
        tk.Label(self.window, text="角色名称:", font=("Arial", 12)).pack(pady=5)
        self.name_entry = tk.Entry(self.window, font=("Arial", 12), width=30)
        self.name_entry.pack(pady=5)
        
        # 背景选择
        tk.Label(self.window, text="背景:", font=("Arial", 12)).pack(pady=5)
        self.background_var = tk.StringVar()
        self.background_combo = ttk.Combobox(self.window, textvariable=self.background_var, 
                                            values=self.game_engine.game.backgrounds, 
                                            font=("Arial", 12), width=30)
        self.background_combo.pack(pady=5)
        
        # 职业选择
        tk.Label(self.window, text="职业:", font=("Arial", 12)).pack(pady=5)
        self.class_var = tk.StringVar()
        self.class_combo = ttk.Combobox(self.window, textvariable=self.class_var,
                                        values=self.game_engine.game.character_classes,
                                        font=("Arial", 12), width=30)
        self.class_combo.pack(pady=5)
        
        # 属性显示
        tk.Label(self.window, text="初始属性:", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.attributes_frame = tk.Frame(self.window)
        self.attributes_frame.pack(pady=5)
        
        # 属性显示
        attributes = ["力量", "敏捷", "体质", "智力", "感知", "魅力"]
        self.attribute_vars = {}
        
        for i, attr in enumerate(attributes):
            tk.Label(self.attributes_frame, text=f"{attr}:", font=("Arial", 10)).grid(row=i//3, column=(i%3)*2, padx=5, pady=2)
            var = tk.StringVar(value="10")
            entry = tk.Entry(self.attributes_frame, textvariable=var, width=5, font=("Arial", 10))
            entry.grid(row=i//3, column=(i%3)*2+1, padx=5, pady=2)
            self.attribute_vars[attr] = var
        
        # 技能预览
        tk.Label(self.window, text="初始技能:", font=("Arial", 12, "bold")).pack(pady=10)
        self.skills_text = scrolledtext.ScrolledText(self.window, height=5, width=60, font=("Arial", 10))
        self.skills_text.pack(pady=5)
        
        # 创建角色按钮
        self.create_button = tk.Button(self.window, text="创建角色", command=self.create_character,
                                      bg="#4CAF50", fg="white", font=("Arial", 12))
        self.create_button.pack(pady=10)
        
        # 绑定选择事件
        self.background_var.trace('w', self.on_background_change)
        self.class_var.trace('w', self.on_class_change)
        
    def on_background_change(self, *args):
        """背景选择改变时更新"""
        self.update_class_preview()
        
    def on_class_change(self, *args):
        """职业选择改变时更新"""
        self.update_class_preview()
        
    def update_class_preview(self):
        """更新职业预览"""
        character_class = self.class_var.get()
        
        if character_class:
            # 更新属性
            if character_class == "战士":
                self.attribute_vars["力量"].set("16")
                self.attribute_vars["体质"].set("14")
                self.attribute_vars["敏捷"].set("10")
                self.attribute_vars["智力"].set("10")
                self.attribute_vars["感知"].set("10")
                self.attribute_vars["魅力"].set("12")
            elif character_class == "法师":
                self.attribute_vars["智力"].set("16")
                self.attribute_vars["感知"].set("14")
                self.attribute_vars["力量"].set("8")
                self.attribute_vars["敏捷"].set("12")
                self.attribute_vars["体质"].set("10")
                self.attribute_vars["魅力"].set("10")
            elif character_class == "牧师":
                self.attribute_vars["感知"].set("16")
                self.attribute_vars["魅力"].set("14")
                self.attribute_vars["力量"].set("10")
                self.attribute_vars["敏捷"].set("10")
                self.attribute_vars["体质"].set("12")
                self.attribute_vars["智力"].set("12")
            elif character_class == "游侠":
                self.attribute_vars["敏捷"].set("16")
                self.attribute_vars["感知"].set("14")
                self.attribute_vars["力量"].set("12")
                self.attribute_vars["智力"].set("10")
                self.attribute_vars["体质"].set("12")
                self.attribute_vars["魅力"].set("10")
            elif character_class == "盗贼":
                self.attribute_vars["敏捷"].set("16")
                self.attribute_vars["魅力"].set("14")
                self.attribute_vars["力量"].set("10")
                self.attribute_vars["感知"].set("12")
                self.attribute_vars["体质"].set("10")
                self.attribute_vars["智力"].set("12")
            
            # 更新技能预览
            self.update_skills_preview(character_class)
    
    def update_skills_preview(self, character_class):
        """更新技能预览"""
        self.skills_text.delete(1.0, tk.END)
        
        if character_class == "战士":
            skills = ["剑术 (战斗 +1)", "格挡 (战斗 +1)", "战斗姿态 (战斗 +1)"]
        elif character_class == "法师":
            skills = ["火球术 (2d6火球伤害)", "治疗术 (2d8治疗)", "法术专精 (魔法 +1)"]
        elif character_class == "牧师":
            skills = ["圣光术 (2d6光明伤害)", "祝福 (神圣祝福)", "神圣治愈 (治疗 +1d4)"]
        elif character_class == "游侠":
            skills = ["弓术 (战斗 +1)", "潜行 (潜行 +1)", "自然亲和 (生存 +1)"]
        elif character_class == "盗贼":
            skills = ["开锁 (潜行 +1)", "偷窃 (潜行 +1)", "暗杀 (战斗 +1)"]
        else:
            skills = ["基础技能"]
            
        self.skills_text.insert(tk.END, "初始技能:\n" + "\n".join(skills))
    
    def create_character(self):
        """创建角色"""
        name = self.name_entry.get().strip()
        background = self.background_var.get()
        character_class = self.class_var.get()
        
        if not name or not background or not character_class:
            messagebox.showerror("错误", "请填写完整的角色信息！")
            return
        
        if self.game_engine.create_character(name, background, character_class):
            messagebox.showinfo("成功", f"角色 {name} 创建成功！")
            self.window.destroy()
        else:
            messagebox.showerror("错误", "角色创建失败！")


class StatusWindow:
    """角色状态窗口"""
    
    def __init__(self, parent, game_engine):
        self.parent = parent
        self.game_engine = game_engine
        self.window = tk.Toplevel(parent)
        self.window.title("角色状态")
        self.window.geometry("500x600")
        
        self.create_widgets()
        self.update_status()
        
    def create_widgets(self):
        """创建界面元素"""
        # 角色基本信息
        self.info_frame = tk.LabelFrame(self.window, text="基本信息", font=("Arial", 12, "bold"))
        self.info_frame.pack(fill="x", padx=10, pady=5)
        
        self.name_label = tk.Label(self.info_frame, text="名称: ", font=("Arial", 11))
        self.name_label.pack(anchor="w", padx=5, pady=2)
        
        self.level_label = tk.Label(self.info_frame, text="等级: ", font=("Arial", 11))
        self.level_label.pack(anchor="w", padx=5, pady=2)
        
        self.exp_label = tk.Label(self.info_frame, text="经验值: ", font=("Arial", 11))
        self.exp_label.pack(anchor="w", padx=5, pady=2)
        
        self.health_label = tk.Label(self.info_frame, text="生命值: ", font=("Arial", 11))
        self.health_label.pack(anchor="w", padx=5, pady=2)
        
        self.gold_label = tk.Label(self.info_frame, text="金币: ", font=("Arial", 11))
        self.gold_label.pack(anchor="w", padx=5, pady=2)
        
        self.chapter_label = tk.Label(self.info_frame, text="当前章节: ", font=("Arial", 11))
        self.chapter_label.pack(anchor="w", padx=5, pady=2)
        
        # 属性面板
        self.attr_frame = tk.LabelFrame(self.window, text="属性", font=("Arial", 12, "bold"))
        self.attr_frame.pack(fill="x", padx=10, pady=5)
        
        self.attr_labels = {}
        attributes = ["力量", "敏捷", "体质", "智力", "感知", "魅力"]
        for attr in attributes:
            label = tk.Label(self.attr_frame, text=f"{attr}: ", font=("Arial", 11))
            label.pack(anchor="w", padx=5, pady=2)
            self.attr_labels[attr] = label
        
        # 道德值面板（含可用对话选项）
        self.morality_frame = tk.LabelFrame(self.window, text="道德值 (-10~+10)", font=("Arial", 12, "bold"))
        self.morality_frame.pack(fill="x", padx=10, pady=5)
        
        self.light_label = tk.Label(self.morality_frame, text="光明值: ", font=("Arial", 11))
        self.light_label.pack(anchor="w", padx=5, pady=2)
        
        self.shadow_label = tk.Label(self.morality_frame, text="暗影值: ", font=("Arial", 11))
        self.shadow_label.pack(anchor="w", padx=5, pady=2)
        
        self.balance_label = tk.Label(self.morality_frame, text="平衡值: ", font=("Arial", 11))
        self.balance_label.pack(anchor="w", padx=5, pady=2)
        
        self.dialogue_label = tk.Label(self.morality_frame, text="可用对话: ", font=("Arial", 11))
        self.dialogue_label.pack(anchor="w", padx=5, pady=2)
        
        # 装备面板
        self.equip_frame = tk.LabelFrame(self.window, text="装备", font=("Arial", 12, "bold"))
        self.equip_frame.pack(fill="x", padx=10, pady=5)
        
        self.equip_listbox = tk.Listbox(self.equip_frame, height=4, font=("Arial", 10))
        self.equip_listbox.pack(fill="x", padx=5, pady=2)
        
        # 技能面板
        self.skill_frame = tk.LabelFrame(self.window, text="技能", font=("Arial", 12, "bold"))
        self.skill_frame.pack(fill="x", padx=10, pady=5)
        
        self.skill_listbox = tk.Listbox(self.skill_frame, height=4, font=("Arial", 10))
        self.skill_listbox.pack(fill="x", padx=5, pady=2)
        
        # 法术面板
        self.spell_frame = tk.LabelFrame(self.window, text="法术", font=("Arial", 12, "bold"))
        self.spell_frame.pack(fill="x", padx=10, pady=5)
        
        self.spell_listbox = tk.Listbox(self.spell_frame, height=4, font=("Arial", 10))
        self.spell_listbox.pack(fill="x", padx=5, pady=2)
        
        # 技能树面板
        self.tree_frame = tk.LabelFrame(self.window, text="技能树", font=("Arial", 12, "bold"))
        self.tree_frame.pack(fill="x", padx=10, pady=5)
        
        self.tree_listbox = tk.Listbox(self.tree_frame, height=4, font=("Arial", 10))
        self.tree_listbox.pack(fill="x", padx=5, pady=2)
        
        # 环境面板
        self.env_frame = tk.LabelFrame(self.window, text="战斗环境", font=("Arial", 12, "bold"))
        self.env_frame.pack(fill="x", padx=10, pady=5)
        
        self.env_label = tk.Label(self.env_frame, text="", font=("Arial", 11))
        self.env_label.pack(anchor="w", padx=5, pady=2)
        
        # 套装效果面板
        self.set_frame = tk.LabelFrame(self.window, text="装备套装效果", font=("Arial", 12, "bold"))
        self.set_frame.pack(fill="x", padx=10, pady=5)
        
        self.set_label = tk.Label(self.set_frame, text="无激活套装", font=("Arial", 11))
        self.set_label.pack(anchor="w", padx=5, pady=2)
        
        # 刷新按钮
        self.refresh_button = tk.Button(self.window, text="刷新状态", command=self.update_status,
                                       bg="#2196F3", fg="white", font=("Arial", 10))
        self.refresh_button.pack(pady=10)
    
    def update_status(self):
        """更新状态显示（包含新增系统信息）"""
        status = self.game_engine.get_player_status()
        
        if "error" in status:
            messagebox.showerror("错误", status["error"])
            return
        
        # 更新基本信息
        self.name_label.config(text=f"名称: {status['name']}")
        self.level_label.config(text=f"等级: {status['level']}")
        self.exp_label.config(text=f"经验值: {status['experience']}")
        self.health_label.config(text=f"生命值: {status['health']}/{status['max_health']}")
        self.gold_label.config(text=f"金币: {status['gold']}")
        self.chapter_label.config(text=f"当前章节: {status['current_chapter']}")
        
        # 更新属性
        self.attr_labels["力量"].config(text=f"力量: {status['attributes']['strength']}")
        self.attr_labels["敏捷"].config(text=f"敏捷: {status['attributes']['dexterity']}")
        self.attr_labels["体质"].config(text=f"体质: {status['attributes']['constitution']}")
        self.attr_labels["智力"].config(text=f"智力: {status['attributes']['intelligence']}")
        self.attr_labels["感知"].config(text=f"感知: {status['attributes']['wisdom']}")
        self.attr_labels["魅力"].config(text=f"魅力: {status['attributes']['charisma']}")
        
        # 更新道德值（含可用对话选项）
        self.light_label.config(text=f"光明值: {status['morality']['light']}")
        self.shadow_label.config(text=f"暗影值: {status['morality']['shadow']}")
        self.balance_label.config(text=f"平衡值: {status['morality']['balance']}")
        dialogues = status.get('available_dialogues', [])
        self.dialogue_label.config(text=f"可用对话: {', '.join(dialogues) if dialogues else '无'}")
        
        # 更新装备
        self.equip_listbox.delete(0, tk.END)
        for equip in status['equipment']:
            self.equip_listbox.insert(tk.END, equip)
        
        # 更新技能
        self.skill_listbox.delete(0, tk.END)
        for skill in status['skills']:
            self.skill_listbox.insert(tk.END, skill)
        
        # 更新法术
        self.spell_listbox.delete(0, tk.END)
        for spell in status['spells']:
            self.spell_listbox.insert(tk.END, spell)
        
        # 更新技能树技能
        self.tree_listbox.delete(0, tk.END)
        tree_skills = status.get('skill_tree_skills', {})
        for name, level in tree_skills.items():
            self.tree_listbox.insert(tk.END, f"{name} (Lv{level})")
        
        # 更新环境信息
        self.env_label.config(text=status.get('environment', '平原 | 晴天'))
        
        # 更新套装效果
        set_bonuses = status.get('set_bonuses', {})
        if set_bonuses:
            bonus_text = ""
            for set_name, data in set_bonuses.items():
                pieces = data['pieces']
                bonus_text += f"{set_name} ({pieces}件): "
                for threshold, bonus in data['activated'].items():
                    bonus_text += f"{bonus.get('description', '')} "
                bonus_text += "\n"
            self.set_label.config(text=bonus_text.strip())
        else:
            self.set_label.config(text="无激活套装")


class CombatWindow:
    """战斗窗口"""
    
    def __init__(self, parent, game_engine):
        self.parent = parent
        self.game_engine = game_engine
        self.window = tk.Toplevel(parent)
        self.window.title("战斗")
        self.window.geometry("700x600")
        
        self.current_monster = None
        self.combat_log = []
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面元素"""
        # 战斗信息面板
        self.info_frame = tk.LabelFrame(self.window, text="战斗信息", font=("Arial", 12, "bold"))
        self.info_frame.pack(fill="x", padx=10, pady=5)
        
        # 怪物信息
        self.monster_frame = tk.LabelFrame(self.info_frame, text="敌人信息", font=("Arial", 10, "bold"))
        self.monster_frame.pack(fill="x", padx=5, pady=5)
        
        self.monster_name_label = tk.Label(self.monster_frame, text="敌人: ", font=("Arial", 10))
        self.monster_name_label.pack(anchor="w", padx=5)
        
        self.monster_health_label = tk.Label(self.monster_frame, text="生命值: ", font=("Arial", 10))
        self.monster_health_label.pack(anchor="w", padx=5)
        
        self.monster_attack_label = tk.Label(self.monster_frame, text="攻击力: ", font=("Arial", 10))
        self.monster_attack_label.pack(anchor="w", padx=5)
        
        # 玩家信息
        self.player_frame = tk.LabelFrame(self.info_frame, text="玩家信息", font=("Arial", 10, "bold"))
        self.player_frame.pack(fill="x", padx=5, pady=5)
        
        self.player_health_label = tk.Label(self.player_frame, text="生命值: ", font=("Arial", 10))
        self.player_health_label.pack(anchor="w", padx=5)
        
        self.player_attack_label = tk.Label(self.player_frame, text="攻击力: ", font=("Arial", 10))
        self.player_attack_label.pack(anchor="w", padx=5)
        
        # 战斗操作面板
        self.action_frame = tk.LabelFrame(self.window, text="战斗操作", font=("Arial", 12, "bold"))
        self.action_frame.pack(fill="x", padx=10, pady=5)
        
        # 环境信息显示
        self.env_info_frame = tk.Frame(self.action_frame)
        self.env_info_frame.pack(fill="x", padx=5, pady=2)
        
        self.env_label = tk.Label(self.env_info_frame, text="环境: 平原 | 晴天", 
                                 font=("Arial", 10), bg="#E3F2FD", relief="solid")
        self.env_label.pack(side="left", padx=5)
        
        self.env_modifier_label = tk.Label(self.env_info_frame, text="修正: +0", 
                                         font=("Arial", 10), bg="#FFF3E0", relief="solid")
        self.env_modifier_label.pack(side="left", padx=5)
        
        # 战斗按钮行1
        button_row1 = tk.Frame(self.action_frame)
        button_row1.pack(fill="x", padx=5, pady=2)
        
        # 攻击按钮
        self.attack_button = tk.Button(button_row1, text="普通攻击", command=self.attack,
                                      bg="#f44336", fg="white", font=("Arial", 10))
        self.attack_button.pack(side="left", padx=5, pady=2)
        
        # 法术按钮
        self.spell_button = tk.Button(button_row1, text="使用法术", command=self.use_spell,
                                     bg="#9c27b0", fg="white", font=("Arial", 10))
        self.spell_button.pack(side="left", padx=5, pady=2)
        
        # 技能按钮
        self.skill_button = tk.Button(button_row1, text="使用技能", command=self.use_skill,
                                      bg="#ff9800", fg="white", font=("Arial", 10))
        self.skill_button.pack(side="left", padx=5, pady=2)
        
        # 战斗按钮行2
        button_row2 = tk.Frame(self.action_frame)
        button_row2.pack(fill="x", padx=5, pady=2)
        
        # 协同法术按钮
        self.synergy_button = tk.Button(button_row2, text="协同法术", command=self.use_synergy_spell,
                                        bg="#00BCD4", fg="white", font=("Arial", 10))
        self.synergy_button.pack(side="left", padx=5, pady=2)
        
        # 团队组合按钮
        self.team_combo_button = tk.Button(button_row2, text="团队组合", command=self.use_team_combo,
                                           bg="#9C27B0", fg="white", font=("Arial", 10))
        self.team_combo_button.pack(side="left", padx=5, pady=2)
        
        # 道德选择按钮
        self.morality_button = tk.Button(button_row2, text="道德选择", command=self.morality_choice,
                                        bg="#4caf50", fg="white", font=("Arial", 10))
        self.morality_button.pack(side="left", padx=5, pady=2)
        
        # 战斗日志
        self.log_frame = tk.LabelFrame(self.window, text="战斗日志", font=("Arial", 12, "bold"))
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=15, font=("Arial", 10))
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # BOSS战斗信息面板
        self.boss_frame = tk.LabelFrame(self.window, text="BOSS战斗信息", font=("Arial", 12, "bold"))
        self.boss_frame.pack(fill="x", padx=10, pady=5)
        
        self.boss_phase_label = tk.Label(self.boss_frame, text="当前阶段: 普通", font=("Arial", 11))
        self.boss_phase_label.pack(anchor="w", padx=5, pady=2)
        
        self.boss_weakness_label = tk.Label(self.boss_frame, text="弱点: 无", font=("Arial", 11))
        self.boss_weakness_label.pack(anchor="w", padx=5, pady=2)
        
        self.boss_ability_label = tk.Label(self.boss_frame, text="特殊能力: 无", font=("Arial", 11))
        self.boss_ability_label.pack(anchor="w", padx=5, pady=2)
        
        # 刷新战斗信息
        self.update_combat_info()
        
    def update_combat_info(self):
        """更新战斗信息"""
        status = self.game_engine.get_player_status()
        
        if "error" not in status:
            self.player_health_label.config(text=f"生命值: {status['health']}/{status['max_health']}")
            player_attack = status['attributes']['strength'] + 2  # 简化的攻击力计算
            self.player_attack_label.config(text=f"攻击力: {player_attack}")
            
            # 更新环境信息显示
            env_info = status.get('environment', '平原 | 晴天')
            self.env_label.config(text=f"环境: {env_info}")
            
            # 更新环境修正显示
            env_modifier = status.get('environment_modifier', 0)
            modifier_text = f"修正: {env_modifier:+d}"
            self.env_modifier_label.config(text=modifier_text)
        
        # 获取当前章节的怪物
        chapter = self.game_engine.get_current_chapter_info()
        if chapter and chapter['monsters']:
            # 随机选择一个怪物
            monster_name = random.choice(chapter['monsters'])
            self.current_monster = next((m for m in self.game_engine.game.monster_database 
                                       if m.name == monster_name), None)
            
            if self.current_monster:
                self.monster_name_label.config(text=f"敌人: {self.current_monster.name}")
                self.monster_health_label.config(text=f"生命值: {self.current_monster.health}")
                self.monster_attack_label.config(text=f"攻击力: {self.current_monster.attack}")
                
                # 检查是否是BOSS战
                if hasattr(self.current_monster, 'is_boss') and self.current_monster.is_boss:
                    self.monster_frame.config(bg="#FFCDD2")  # 红色背景表示BOSS
                    self.monster_name_label.config(text=f"BOSS: {self.current_monster.name}", font=("Arial", 12, "bold"))
                else:
                    self.monster_frame.config(bg="white")
                    self.monster_name_label.config(text=f"敌人: {self.current_monster.name}", font=("Arial", 10))
    
    def attack(self):
        """普通攻击（含环境修正）"""
        if not self.current_monster:
            self.log("没有可攻击的目标！")
            return
        
        combat_result = self.game_engine.combat_round("攻击", self.current_monster)
        
        # 显示环境修正
        env_info = combat_result.get('environment', '')
        if env_info:
            self.log(f"环境: {env_info}")
        
        # 添加战斗日志
        self.log(f"你攻击了{self.current_monster.name}！")
        self.log(f"攻击检定: {combat_result['player_attack']}")
        self.log(f"造成伤害: {combat_result['player_damage']}")
        
        if combat_result['target_damage'] > 0:
            self.log(f"你受到了{combat_result['target_damage']}点伤害！")
        
        if not combat_result['target_alive']:
            self.log(f"{self.current_monster.name}被击败了！")
            self.log(f"获得{self.current_monster.experience}点经验值！")
            self.game_engine.player.gain_experience(self.current_monster.experience)
        
        if not combat_result['player_alive']:
            self.log("你被击败了！游戏结束。")
            self.window.destroy()
        
        # 刷新战斗信息
        self.update_combat_info()
    
    def use_spell(self):
        """使用法术"""
        if not self.game_engine.player.spells:
            self.log("你没有学会任何法术！")
            return
        
        if not self.current_monster:
            self.log("没有法术目标！")
            return
        
        # 显示可用的法术
        spell_names = [spell.name for spell in self.game_engine.player.spells]
        spell_dialog = tk.Toplevel(self.window)
        spell_dialog.title("选择法术")
        spell_dialog.geometry("300x200")
        
        tk.Label(spell_dialog, text="选择要使用的法术:").pack(pady=5)
        
        spell_var = tk.StringVar()
        spell_combo = ttk.Combobox(spell_dialog, textvariable=spell_var, values=spell_names)
        spell_combo.pack(pady=5)
        
        def cast_spell():
            spell_name = spell_var.get()
            if spell_name:
                result = self.game_engine.cast_spell(spell_name, self.current_monster)
                self.log(f"使用法术: {result['spell_name']}")
                self.log(f"造成伤害: {result['damage']}")
                self.log(f"效果: {result['effect']}")
                
                spell_dialog.destroy()
                self.update_combat_info()
        
        tk.Button(spell_dialog, text="施放", command=cast_spell).pack(pady=5)
    
    def use_skill(self):
        """使用技能"""
        if not self.game_engine.player.skills:
            self.log("你没有学会任何技能！")
            return
        
        # 显示可用的技能（包括技能树技能）
        player = self.game_engine.game.player
        
        # 基础技能
        basic_skills = [skill.name for skill in self.game_engine.player.skills]
        
        # 技能树技能
        tree_skills = []
        if hasattr(player, 'skill_tree') and player.skill_tree.owned_skills:
            for skill_name, level in player.skill_tree.owned_skills.items():
                if level > 0:
                    tree_skills.append(f"{skill_name} (树Lv{level})")
        
        all_skills = basic_skills + tree_skills
        if not all_skills:
            self.log("你没有学会任何技能！")
            return
        
        skill_dialog = tk.Toplevel(self.window)
        skill_dialog.title("选择技能")
        skill_dialog.geometry("400x300")
        
        tk.Label(skill_dialog, text="选择要使用的技能:", font=("Arial", 12, "bold")).pack(pady=5)
        
        # 技能列表
        skill_listbox = tk.Listbox(skill_dialog, height=8, font=("Arial", 10))
        skill_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        for skill_name in all_skills:
            skill_listbox.insert(tk.END, skill_name)
        
        def use_skill():
            selection = skill_listbox.curselection()
            if selection:
                skill_name = skill_listbox.get(selection[0])
                
                # 检查是否是技能树技能
                if " (树" in skill_name:
                    # 提取技能树技能名和等级
                    tree_name = skill_name.split(" (树")[0]
                    result = self.game_engine.use_tree_skill(tree_name)
                else:
                    # 基础技能
                    result = self.game_engine.use_skill(skill_name)
                
                self.log(f"使用技能: {result['skill_name']}")
                self.log(f"检定结果: {result['result']}")
                self.log(f"技能加成: {result['bonus']}")
                
                skill_dialog.destroy()
                self.update_combat_info()
        
        button_frame = tk.Frame(skill_dialog)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="使用", command=use_skill,
                 bg="#ff9800", fg="white", font=("Arial", 10)).pack(side="right", padx=5)
        tk.Button(button_frame, text="取消", command=skill_dialog.destroy,
                 bg="#757575", fg="white", font=("Arial", 10)).pack(side="right", padx=5)
    
    def use_synergy_spell(self):
        """使用协同法术（两个法术组合产生特殊效果）"""
        if not self.game_engine.game.player.spells:
            self.log("你没有学会任何法术！")
            return
        if len(self.game_engine.game.player.spells) < 2:
            self.log("至少需要两个法术才能使用协同！")
            return
        if not self.current_monster:
            self.log("没有法术目标！")
            return
        
        spell_names = [spell.name for spell in self.game_engine.game.player.spells]
        synergy_dialog = tk.Toplevel(self.window)
        synergy_dialog.title("协同法术选择")
        synergy_dialog.geometry("500x350")
        
        # 标题
        tk.Label(synergy_dialog, text="选择两个法术进行协同施法", 
                font=("Arial", 12, "bold")).pack(pady=5)
        
        # 选择第一个法术
        select_frame1 = tk.Frame(synergy_dialog)
        select_frame1.pack(fill="x", padx=10, pady=5)
        
        tk.Label(select_frame1, text="第一个法术:", font=("Arial", 10)).pack(side="left", padx=5)
        spell_a_var = tk.StringVar()
        spell_a_combo = ttk.Combobox(select_frame1, textvariable=spell_a_var, values=spell_names)
        spell_a_combo.pack(side="left", padx=5, fill="x", expand=True)
        spell_a_combo.bind('<<ComboboxSelected>>', lambda e: self._update_spell_info(spell_a_combo, spell_info_frame1))
        
        # 选择第二个法术
        select_frame2 = tk.Frame(synergy_dialog)
        select_frame2.pack(fill="x", padx=10, pady=5)
        
        tk.Label(select_frame2, text="第二个法术:", font=("Arial", 10)).pack(side="left", padx=5)
        spell_b_var = tk.StringVar()
        spell_b_combo = ttk.Combobox(select_frame2, textvariable=spell_b_var, values=spell_names)
        spell_b_combo.pack(side="left", padx=5, fill="x", expand=True)
        spell_b_combo.bind('<<ComboboxSelected>>', lambda e: self._update_spell_info(spell_b_combo, spell_info_frame2))
        
        # 协同信息显示
        synergy_info_frame = tk.LabelFrame(synergy_dialog, text="协同效果", font=("Arial", 10, "bold"))
        synergy_info_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        synergy_text = tk.Text(synergy_info_frame, height=6, font=("Arial", 9), wrap="word")
        synergy_text.pack(fill="both", expand=True, padx=5, pady=5)
        synergy_text.insert(tk.END, "选择两个不同的法术查看协同效果...")
        
        def cast_synergy():
            a = spell_a_var.get()
            b = spell_b_var.get()
            if a and b and a != b:
                result = self.game_engine.cast_synergized_spells(a, b, self.current_monster)
                if "error" in result:
                    self.log(result["error"])
                    messagebox.showerror("错误", result["error"])
                else:
                    self.log(f"协同法术: {result['synergy']} - {result.get('description', '')}")
                    self.log(f"总伤害: {result.get('total_damage', 0)}")
                    messagebox.showinfo("协同施法", 
                                      f"协同效果: {result.get('synergy', '')}\n"
                                      f"描述: {result.get('description', '')}\n"
                                      f"总伤害: {result.get('total_damage', 0)}")
                synergy_dialog.destroy()
                self.update_combat_info()
        
        # 按钮区域
        button_frame = tk.Frame(synergy_dialog)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="施放协同", command=cast_synergy,
                 bg="#00BCD4", fg="white", font=("Arial", 10)).pack(side="right", padx=5)
        
        tk.Button(button_frame, text="取消", command=synergy_dialog.destroy,
                 bg="#757575", fg="white", font=("Arial", 10)).pack(side="right", padx=5)
    
    def _update_spell_info(self, combo_widget, info_frame):
        """更新法术信息显示"""
        spell_name = combo_widget.get()
        if spell_name:
            # 这里可以添加更详细的法术信息显示
            pass
    
    def morality_choice(self):
        """道德选择"""
        morality_dialog = tk.Toplevel(self.window)
        morality_dialog.title("道德选择")
        morality_dialog.geometry("300x250")
        
        tk.Label(morality_dialog, text="选择你的行动方式:").pack(pady=10)
        
        # 光明选择
        light_button = tk.Button(morality_dialog, text="做出光明选择 (+2光明值)", 
                                command=lambda: self.make_morality_choice("light", 2))
        light_button.pack(pady=5)
        
        # 暗影选择
        shadow_button = tk.Button(morality_dialog, text="做出暗影选择 (+2暗影值)", 
                                 command=lambda: self.make_morality_choice("shadow", 2))
        shadow_button.pack(pady=5)
        
        # 平衡选择
        balance_button = tk.Button(morality_dialog, text="做出平衡选择 (+2平衡值)", 
                                  command=lambda: self.make_morality_choice("balance", 2))
        balance_button.pack(pady=5)
        
        morality_dialog.destroy()
    
    def use_team_combo(self):
        """使用团队组合技能"""
        if not self.current_monster:
            self.log("没有战斗目标！")
            return
        
        # 显示可用的团队组合
        combo_names = ["双重打击", "掩护射击", "夹击战术", "守护阵型", "协同攻击"]
        combo_dialog = tk.Toplevel(self.window)
        combo_dialog.title("选择团队组合")
        combo_dialog.geometry("350x250")
        
        tk.Label(combo_dialog, text="选择要使用的团队组合:").pack(pady=5)
        
        combo_var = tk.StringVar()
        combo_combo = ttk.Combobox(combo_dialog, textvariable=combo_var, values=combo_names)
        combo_combo.pack(pady=5)
        
        # 组合效果说明
        effect_frame = tk.Frame(combo_dialog)
        effect_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        def show_combo_effect(event):
            combo_name = combo_var.get()
            if combo_name:
                effects = {
                    "双重打击": "两次连续攻击，每次造成50%伤害",
                    "掩护射击": "攻击+防御，降低目标攻击力",
                    "夹击战术": "团队协作，造成额外伤害",
                    "守护阵型": "防御姿态，减少受到的伤害",
                    "协同攻击": "多人配合，爆发性伤害"
                }
                effect_label.config(text=f"效果: {effects.get(combo_name, '未知效果')}")
        
        effect_label = tk.Label(effect_frame, text="选择组合查看效果", font=("Arial", 9), 
                              wraplength=300, justify="left")
        effect_label.pack(fill="both", expand=True)
        
        combo_combo.bind('<<ComboboxSelected>>', show_combo_effect)
        
        def execute_combo():
            combo_name = combo_var.get()
            if combo_name:
                result = self.game_engine.execute_team_combo(combo_name, self.current_monster)
                if "error" in result:
                    self.log(result["error"])
                else:
                    self.log(f"使用了团队组合: {result['combo_name']}")
                    self.log(f"效果: {result['effect']}")
                    self.log(f"造成伤害: {result['damage']}")
                
                combo_dialog.destroy()
                self.update_combat_info()
        
        tk.Button(combo_dialog, text="执行", command=execute_combo, 
                 bg="#9C27B0", fg="white", font=("Arial", 10)).pack(pady=5)
    
    def make_morality_choice(self, choice_type, amount):
        """做出道德选择"""
        result = self.game_engine.make_morality_choice(choice_type, amount)
        self.log(f"做出了{result['choice_type']}选择！")
        self.log(f"获得{result['choice_type']}值 {amount}")
        
        # 显示当前道德值
        values = result['current_values']
        self.log(f"当前道德值: 光明={values['light']}, 暗影={values['shadow']}, 平衡={values['balance']}")
    
    def log(self, message):
        """添加战斗日志"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)


class QuestWindow:
    """任务窗口"""
    
    def __init__(self, parent, game_engine):
        self.parent = parent
        self.game_engine = game_engine
        self.window = tk.Toplevel(parent)
        self.window.title("任务管理")
        self.window.geometry("600x500")
        
        self.create_widgets()
        self.update_quests()
        
    def create_widgets(self):
        """创建界面元素"""
        # 当前任务
        self.current_frame = tk.LabelFrame(self.window, text="当前任务", font=("Arial", 12, "bold"))
        self.current_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.quest_tree = ttk.Treeview(self.current_frame, columns=("描述", "进度"), show="tree headings", height=10)
        self.quest_tree.heading("#0", text="任务名称")
        self.quest_tree.heading("描述", text="描述")
        self.quest_tree.heading("进度", text="进度")
        self.quest_tree.column("#0", width=150)
        self.quest_tree.column("描述", width=300)
        self.quest_tree.column("进度", width=100)
        self.quest_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 完成的任务
        self.completed_frame = tk.LabelFrame(self.window, text="已完成任务", font=("Arial", 12, "bold"))
        self.completed_frame.pack(fill="x", padx=10, pady=5)
        
        self.completed_listbox = tk.Listbox(self.completed_frame, height=4, font=("Arial", 10))
        self.completed_listbox.pack(fill="x", padx=5, pady=5)
        
        # 操作按钮
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(fill="x", padx=10, pady=5)
        
        self.refresh_button = tk.Button(self.button_frame, text="刷新任务", command=self.update_quests,
                                      bg="#2196F3", fg="white", font=("Arial", 10))
        self.refresh_button.pack(side="left", padx=5)
        
        self.complete_button = tk.Button(self.button_frame, text="完成任务", command=self.complete_quest,
                                        bg="#4CAF50", fg="white", font=("Arial", 10))
        self.complete_button.pack(side="left", padx=5)
    
    def update_quests(self):
        """更新任务列表"""
        # 清空当前任务
        for item in self.quest_tree.get_children():
            self.quest_tree.delete(item)
        
        # 获取当前章节任务
        chapter = self.game_engine.get_current_chapter_info()
        if chapter and chapter['quests']:
            for quest_name in chapter['quests']:
                # 这里简化处理，实际应该从quest数据库获取详细信息
                self.quest_tree.insert("", "end", text=quest_name, values=("探索该区域", "未开始"))
        
        # 更新已完成任务
        self.completed_listbox.delete(0, tk.END)
        if self.game_engine.player:
            for quest in self.game_engine.player.completed_quests:
                self.completed_listbox.insert(tk.END, quest)
    
    def complete_quest(self):
        """完成任务"""
        selected_item = self.quest_tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请选择要完成的任务！")
            return
        
        quest_name = self.quest_tree.item(selected_item[0])['text']
        result = self.game_engine.complete_quest(quest_name)
        
        if "error" in result:
            messagebox.showerror("错误", result["error"])
        else:
            messagebox.showinfo("成功", f"任务 {result['quest_completed']} 已完成！")
            self.update_quests()


class MainWindow:
    """主游戏窗口"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("暗影王座的救赎")
        self.root.geometry("800x600")
        
        # 游戏引擎
        self.game_engine = GameEngine()
        
        # 创建主界面
        self.create_widgets()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """创建界面元素"""
        # 标题
        self.title_label = tk.Label(self.root, text="暗影王座的救赎", 
                                   font=("Arial", 20, "bold"), fg="darkblue")
        self.title_label.pack(pady=20)
        
        # 主菜单框架
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)
        
        # 菜单按钮
        self.create_character_button = tk.Button(self.menu_frame, text="创建角色", 
                                               command=self.create_character,
                                               bg="#4CAF50", fg="white", font=("Arial", 12), width=15)
        self.create_character_button.grid(row=0, column=0, padx=10, pady=5)
        
        self.status_button = tk.Button(self.menu_frame, text="查看状态", 
                                      command=self.show_status,
                                      bg="#2196F3", fg="white", font=("Arial", 12), width=15)
        self.status_button.grid(row=0, column=1, padx=10, pady=5)
        
        self.combat_button = tk.Button(self.menu_frame, text="开始战斗", 
                                      command=self.start_combat,
                                      bg="#f44336", fg="white", font=("Arial", 12), width=15)
        self.combat_button.grid(row=1, column=0, padx=10, pady=5)
        
        self.quest_button = tk.Button(self.menu_frame, text="任务管理", 
                                     command=self.show_quests,
                                     bg="#ff9800", fg="white", font=("Arial", 12), width=15)
        self.quest_button.grid(row=1, column=1, padx=10, pady=5)
        
        self.next_chapter_button = tk.Button(self.menu_frame, text="下一章节", 
                                           command=self.next_chapter,
                                           bg="#9c27b0", fg="white", font=("Arial", 12), width=15)
        self.next_chapter_button.grid(row=2, column=0, padx=10, pady=5)
        
        self.end_game_button = tk.Button(self.menu_frame, text="结束游戏", 
                                        command=self.end_game,
                                        bg="#607d8b", fg="white", font=("Arial", 12), width=15)
        self.end_game_button.grid(row=2, column=1, padx=10, pady=5)
        
        self.env_button = tk.Button(self.menu_frame, text="设置环境", 
                                    command=self.set_environment,
                                    bg="#795548", fg="white", font=("Arial", 12), width=15)
        self.env_button.grid(row=3, column=0, padx=10, pady=5)
        
        self.save_button = tk.Button(self.menu_frame, text="保存游戏", 
                                     command=self.save_game,
                                     bg="#009688", fg="white", font=("Arial", 12), width=15)
        self.save_button.grid(row=3, column=1, padx=10, pady=5)
        
        self.load_button = tk.Button(self.menu_frame, text="加载游戏", 
                                     command=self.load_game,
                                     bg="#FF5722", fg="white", font=("Arial", 12), width=15)
        self.load_button.grid(row=4, column=0, padx=10, pady=5)
        
        self.skill_tree_button = tk.Button(self.menu_frame, text="技能树", 
                                           command=self.show_skill_tree,
                                           bg="#3F51B5", fg="white", font=("Arial", 12), width=15)
        self.skill_tree_button.grid(row=4, column=1, padx=10, pady=5)
        
        # 信息显示区域
        self.info_frame = tk.LabelFrame(self.root, text="游戏信息", font=("Arial", 12, "bold"))
        self.info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=10, font=("Arial", 10))
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 显示欢迎信息
        self.show_welcome_message()
        
    def show_welcome_message(self):
        """显示欢迎信息"""
        welcome_text = """
欢迎来到《暗影王座的救赎》！

这是一个基于DND规则的桌面角色扮演游戏。
你将踏上一段从边境村庄到暗影王座的史诗之旅。

游戏特色：
- 三维道德系统：光明、暗影、平衡
- 四章节完整剧情：从1级到20级的完整成长
- 三种不同结局：光明救赎、黑暗统治、平衡之道
- 丰富的角色选择：405种背景，134种职业

开始你的冒险吧！
        """
        self.info_text.insert(tk.END, welcome_text)
        
    def create_character(self):
        """创建角色"""
        CharacterCreationWindow(self.root, self.game_engine)
        
    def show_status(self):
        """显示角色状态"""
        if not self.game_engine.game.player:
            messagebox.showwarning("警告", "请先创建角色！")
            return
        StatusWindow(self.root, self.game_engine)
        
    def start_combat(self):
        """开始战斗"""
        if not self.game_engine.game.player:
            messagebox.showwarning("警告", "请先创建角色！")
            return
        CombatWindow(self.root, self.game_engine)
        
    def show_quests(self):
        """显示任务"""
        if not self.game_engine.game.player:
            messagebox.showwarning("警告", "请先创建角色！")
            return
        QuestWindow(self.root, self.game_engine)
        
    def next_chapter(self):
        """进入下一章节"""
        if not self.game_engine.game.player:
            messagebox.showwarning("警告", "请先创建角色！")
            return
        
        current_chapter = self.game_engine.game.player.current_chapter
        if current_chapter < len(self.game_engine.game.chapters):
            self.game_engine.next_chapter()
            messagebox.showinfo("章节转换", f"进入第 {self.game_engine.game.player.current_chapter} 章: {self.game_engine.game.current_chapter.name}")
            
            # 显示章节信息
            self.show_chapter_info()
        else:
            messagebox.showinfo("提示", "已经是最后一章了！")
    
    def show_chapter_info(self):
        """显示章节信息"""
        chapter = self.game_engine.get_current_chapter_info()
        chapter_info = f"""
当前章节：{chapter['name']}
等级范围：{chapter['level_range']}
可用地点：{', '.join(chapter['locations'])}
可用NPC：{', '.join(chapter['npcs'])}
可用怪物：{', '.join(chapter['monsters'])}
可用任务：{', '.join(chapter['quests'])}
        """
        self.info_text.insert(tk.END, chapter_info)
        
    def set_environment(self):
        """设置战斗环境（地形+天气）"""
        env_dialog = tk.Toplevel(self.root)
        env_dialog.title("设置战斗环境")
        env_dialog.geometry("300x250")
        
        import config
        
        tk.Label(env_dialog, text="地形:", font=("Arial", 12)).pack(pady=5)
        terrain_var = tk.StringVar(value=self.game_engine.environment.terrain)
        terrain_combo = ttk.Combobox(env_dialog, textvariable=terrain_var,
                                     values=list(config.TERRAIN_MODIFIERS.keys()))
        terrain_combo.pack(pady=5)
        
        tk.Label(env_dialog, text="天气:", font=("Arial", 12)).pack(pady=5)
        weather_var = tk.StringVar(value=self.game_engine.environment.weather)
        weather_combo = ttk.Combobox(env_dialog, textvariable=weather_var,
                                     values=list(config.WEATHER_MODIFIERS.keys()))
        weather_combo.pack(pady=5)
        
        def apply_env():
            self.game_engine.set_environment(terrain_var.get(), weather_var.get())
            messagebox.showinfo("环境已更新",
                               self.game_engine.environment.get_environment_description())
            env_dialog.destroy()
        
        tk.Button(env_dialog, text="应用", command=apply_env, 
                  bg="#795548", fg="white", font=("Arial", 12)).pack(pady=10)
    
    def save_game(self):
        """保存游戏到存档位"""
        if not self.game_engine.game.player:
            messagebox.showwarning("警告", "请先创建角色！")
            return
        slot = tk.simpledialog.askinteger("保存游戏", "请输入存档位 (1-9):", 
                                          minvalue=1, maxvalue=9, parent=self.root)
        if slot:
            ok, msg = self.game_engine.save_game(slot)
            messagebox.showinfo("保存游戏", msg)
    
    def load_game(self):
        """加载游戏存档"""
        saves = self.game_engine.list_saves()
        if not saves:
            messagebox.showinfo("加载游戏", "没有找到存档！")
            return
        
        load_dialog = tk.Toplevel(self.root)
        load_dialog.title("选择存档")
        load_dialog.geometry("400x300")
        
        tk.Label(load_dialog, text="可用存档:", font=("Arial", 12, "bold")).pack(pady=5)
        
        for s in saves:
            btn = tk.Button(load_dialog, 
                           text=f"存档位 {s['slot']}: {s['player_name']} Lv{s['level']} ({s['timestamp'][:16]})",
                           command=lambda slot=s['slot']: self._do_load(slot, load_dialog),
                           font=("Arial", 10), width=40)
            btn.pack(pady=3)
    
    def _do_load(self, slot, dialog):
        """执行加载"""
        ok, msg = self.game_engine.load_game(slot)
        dialog.destroy()
        messagebox.showinfo("加载游戏", msg)
        if ok:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"已加载存档位 {slot} 的游戏\n")
            status = self.game_engine.get_player_status()
            self.info_text.insert(tk.END, f"角色: {status['name']} Lv{status['level']}\n")
    
    def show_skill_tree(self):
        """显示技能树窗口"""
        if not self.game_engine.game.player:
            messagebox.showwarning("警告", "请先创建角色！")
            return
        
        tree_dialog = tk.Toplevel(self.root)
        tree_dialog.title("技能树")
        tree_dialog.geometry("700x600")
        
        import game_systems
        
        player = self.game_engine.game.player
        
        # 技能树分类标签页
        notebook = ttk.Notebook(tree_dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        for tree_name, tree_skills in game_systems.SkillTree.DEFAULT_TREES.items():
            frame = tk.Frame(notebook)
            notebook.add(frame, text=tree_name)
            
            # 创建技能树框架
            tree_container = tk.Frame(frame)
            tree_container.pack(fill="both", expand=True, padx=5, pady=5)
            
            # 滚动条
            canvas = tk.Canvas(tree_container)
            scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # 按等级分组显示技能
            for skill_name, node in tree_skills.items():
                current_level = player.skill_tree.owned_skills.get(skill_name, 0)
                
                # 创建技能卡片
                skill_card = tk.Frame(scrollable_frame, relief="solid", borderwidth=1, bg="white")
                skill_card.pack(fill="x", padx=3, pady=3)
                
                # 技能名和等级
                level_text = f"Lv{current_level}" if current_level > 0 else "未学习"
                level_color = "#4CAF50" if current_level > 0 else "#757575"
                tk.Label(skill_card, text=f"{skill_name} ({level_text})",
                        font=("Arial", 10, "bold"), fg=level_color).pack(anchor="w", padx=5, pady=2)
                
                # 技能描述
                desc = node.level_descriptions.get(max(1, current_level), node.description)
                tk.Label(skill_card, text=f"效果: {desc}", font=("Arial", 9), 
                        wraplength=600, justify="left").pack(anchor="w", padx=5, pady=1)
                
                # 前置条件
                if hasattr(node, 'prerequisites') and node.prerequisites:
                    prereq_text = f"前置: {', '.join(node.prerequisites)}"
                    tk.Label(skill_card, text=prereq_text, font=("Arial", 8), 
                            fg="#666", wraplength=600).pack(anchor="w", padx=5, pady=1)
                
                # 学习/升级按钮
                button_frame = tk.Frame(skill_card)
                button_frame.pack(anchor="e", padx=5, pady=2)
                
                if current_level == 0:
                    tk.Button(button_frame, text="学习",
                             command=lambda sn=skill_name: self._learn_tree_skill(sn, tree_dialog),
                             bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side="right", padx=2)
                elif current_level < 5:
                    tk.Button(button_frame, text=f"升级→Lv{current_level+1}",
                             command=lambda sn=skill_name: self._upgrade_tree_skill(sn, tree_dialog),
                             bg="#2196F3", fg="white", font=("Arial", 9)).pack(side="right", padx=2)
                
                # 显示当前等级属性加成
                if current_level > 0:
                    bonus = node.get_level_bonus(current_level)
                    bonus_text = f"当前加成: {bonus}"
                    tk.Label(skill_card, text=bonus_text, font=("Arial", 8), 
                            fg="#2196F3", wraplength=600).pack(anchor="w", padx=5, pady=1)
    
    def _learn_tree_skill(self, skill_name, dialog):
        """从技能树学习技能"""
        result = self.game_engine.learn_skill_from_tree(skill_name)
        messagebox.showinfo("技能树", result['message'])
        dialog.destroy()
        self.show_skill_tree()  # 重新打开以刷新
    
    def _upgrade_tree_skill(self, skill_name, dialog):
        """升级技能树中的技能"""
        result = self.game_engine.upgrade_skill_in_tree(skill_name)
        messagebox.showinfo("技能树", result['message'])
        dialog.destroy()
        self.show_skill_tree()  # 重新打开以刷新
    
    def end_game(self):
        """结束游戏"""
        if not self.game_engine.game.player:
            messagebox.showinfo("提示", "请先创建角色！")
            return
        
        ending = self.game_engine.complete_game()
        messagebox.showinfo("游戏结束", ending)
        
        # 询问是否开始新游戏
        if messagebox.askyesno("新游戏", "是否开始新游戏？"):
            self.game_engine.start_new_game()
            self.info_text.delete(1.0, tk.END)
            self.show_welcome_message()
        else:
            self.root.quit()
    
    def on_closing(self):
        """窗口关闭事件"""
        if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
            self.root.quit()
    
    def run(self):
        """运行游戏"""
        self.root.mainloop()


# 主程序入口
if __name__ == "__main__":
    game = MainWindow()
    game.run()