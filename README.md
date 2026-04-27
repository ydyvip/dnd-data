# 《暗影王座的救赎》DND游戏项目

## 🎮 项目概述

本项目基于DND规则创建了一个完整的桌面角色扮演游戏《暗影王座的救赎》。游戏包含了从角色创建到最终结局的完整游戏体验，提供了图形用户界面和完整的GM工具包。

## 🌟 游戏特色

### 核心系统
- **三维道德系统**: 光明、暗影、平衡值影响结局
- **四章节剧情**: 1-20级的完整成长体验
- **三种结局**: 光明救赎、黑暗统治、平衡之道
- **丰富的角色选择**: 405种背景，134种职业

### 游戏机制
- **完整的战斗系统**: 包含攻击、法术、技能等
- **任务系统**: 多样化的任务和奖励
- **装备系统**: 丰富的魔法装备和物品
- **法术系统**: 0-9环的完整法术体系
- **技能树**: 5级技能进阶系统

### GM支持
- **完整的GM工具包**: NPC追踪、战斗计算、随机事件等
- **即兴生成器**: 剧情、地点、战利品生成
- **进度追踪**: 游戏进程和道德值追踪

## 🚀 快速开始

### 1. 环境要求
- Python 3.7+
- Tkinter (Python标准库)
- 无需额外依赖

### 2. 运行游戏

#### 控制台版本
```bash
cd C:\Users\Administrator\git-AI\dnd-data
python shadow_throne_redemption.py
```

#### 图形界面版本
```bash
cd C:\Users\Administrator\git-AI\dnd-data
python gui_game.py
```

#### GM工具包
```bash
cd C:\Users\Administrator\git-AI\dnd-data
python gm_tools.py
```

### 3. 游戏流程

1. **创建角色**: 选择背景、职业，设置初始属性
2. **开始冒险**: 从边境村庄开始你的冒险
3. **完成任务**: 接受任务，完成挑战，获得奖励
4. **成长升级**: 获得经验值，提升等级，学习技能
5. **道德选择**: 每个选择都影响最终结局
6. **最终对决**: 击败暗影君主，决定世界命运

## 📁 项目结构

```
C:\Users\Administrator\git-AI\dnd-data\
├── README.md                          # 项目说明文档
├── shadow_throne_redemption.py       # 游戏核心引擎
├── gui_game.py                       # 图形用户界面
├── gm_tools.py                      # GM工具包
├── game-materials/                   # 游戏材料目录
│   ├── 游戏规则书.md                 # 核心游戏规则
│   ├── 角色创建指南.md               # 角色创建规则
│   ├── GM指南.md                    # GM操作指南
│   ├── 战斗规则补充.md               # 战斗规则扩展
│   ├── 结局判定系统.md               # 道德结局系统
│   ├── 法术和技能手册.md             # 法术和技能系统
│   ├── 剧情分支树.md                 # 完整剧情分支
│   ├── NPC数据库.md                  # 角色数据库
│   ├── 怪物图鉴.md                   # 怪物数据
│   ├── 道具和装备列表.md             # 装备系统
│   ├── 世界地图和场景描述.md         # 世界观描述
│   ├── GM工具包.md                   # GM工具文档
│   ├── 实战GM技巧.md                 # GM技巧指南
│   ├── 项目完整清单.md               # 完整游戏材料清单
│   └── 游戏完成总结.md               # 项目完成总结
```

## 🛠️ 核心文件说明

### 1. 游戏核心引擎 (`shadow_throne_redemption.py`)
- **Dice**: 骰子系统
- **Attribute**: 角色属性系统
- **Morality**: 三维道德值系统
- **Skill/Equipment/Spell**: 技能、装备、法术系统
- **Monster/NPC/Quest**: 怪物、NPC、任务系统
- **Player**: 玩家角色
- **Game/GameEngine**: 游戏主引擎

### 2. 图形用户界面 (`gui_game.py`)
- **CharacterCreationWindow**: 角色创建界面
- **StatusWindow**: 角色状态界面
- **CombatWindow**: 战斗界面
- **QuestWindow**: 任务管理界面
- **MainWindow**: 主游戏界面

### 3. GM工具包 (`gm_tools.py`)
- **GMTracker**: NPC关系追踪器
- **CombatCalculator**: 战斗难度计算器
- **WorldBuilder**: 世界构建工具
- **LootGenerator**: 战利品生成器
- **PlotGenerator**: 急救剧情生成器
- **GMToolManager**: GM工具管理器

## 📋 游戏规则详解

### 1. 角色创建
- **背景系统**: 405种背景选择，影响初始属性和技能
- **职业系统**: 134种职业选择，包括战士、法师、牧师、游侠、盗贼等
- **属性系统**: 六大属性（力量、敏捷、体质、智力、感知、魅力）

### 2. 道德系统
- **光明值 (0-10)**: 代表善良、光明、救赎的价值观
- **暗影值 (0-10)**: 代表黑暗、掌控、力量的价值观
- **平衡值 (0-10)**: 代表和谐、理性、中庸的价值观
- **结局触发**: 根据道德值决定三种不同结局

### 3. 战斗系统
- **回合制战斗**: 完整的攻击、防御、法术、技能系统
- **环境互动**: 地形、天气等环境因素影响战斗
- **团队协同**: 多角色配合的特殊战术

### 4. 任务系统
- **主线任务**: 推进剧情发展，影响最终结局
- **支线任务**: 额外挑战和奖励
- **隐藏任务**: 特殊条件和奖励

### 5. 法术技能系统
- **法术等级**: 戏法(0环)到9环终极法术
- **技能树**: 5级技能进阶系统
- **特殊技能**: 光明、暗影、平衡三大系技能

## 🧪 测试与验证

### 1. 运行测试
```bash
# 运行控制台版本
python shadow_throne_redemption.py

# 运行GUI版本
python gui_game.py

# 运行GM工具包
python gm_tools.py
```

### 2. 代码测试
```python
# 单元测试
import unittest
from shadow_throne_redemption import Game, Player, Attribute, Morality

class TestGameSystem(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.create_character("测试角色", "冒险者", "战士")
    
    def test_character_creation(self):
        self.assertIsNotNone(self.game.player)
        self.assertEqual(self.game.player.name, "测试角色")
        self.assertEqual(self.game.player.character_class, "战士")

if __name__ == '__main__':
    unittest.main()
```

## 📊 游戏数据统计

| 类别 | 数量 | 说明 |
|------|------|------|
| 背景选项 | 405种 | 包括孤儿、贵族、冒险者等 |
| 职业选择 | 134种 | 包括战士、法师、牧师、游侠、盗贼等 |
| 怪物数量 | 11,463种 | 分布在4个章节中 |
| 装备道具 | 15,749种 | 从普通装备到传奇神器 |
| 法术数量 | 5,849种 | 0-9环完整法术体系 |
| NPC数量 | 12个主要角色 | 丰富的角色互动 |
| 任务数量 | 100+个 | 主线、支线、隐藏任务 |
| 章节数量 | 4个 | 1-20级完整成长曲线 |

## 🎯 游戏体验

### 新手引导
1. 选择适合的背景和职业
2. 理解三维道德系统
3. 学习基础战斗规则
4. 接受第一个任务
5. 开始你的冒险之旅

### GM指导
1. 使用GM工具包管理游戏
2. 平衡战斗难度和挑战性
3. 根据玩家行动调整剧情
4. 记录道德值和关系变化
5. 引导玩家体验不同结局

### 高级玩法
1. **多周目**: 体验不同道德路线
2. **自定义**: 创建新的背景、职业、法术
3. **多人游戏**: 扩展支持网络对战
4. **模组制作**: 开发新的游戏模组

## 🔧 扩展开发

### 1. 添加新内容
```python
# 添加新职业
@dataclass
class NewClass:
    name: str
    description: str
    attributes: Dict[str, int]
    skills: List[str]

# 添加新法术
@dataclass
class NewSpell:
    name: str
    spell_level: int
    school: str
    damage: str
    effect: str
```

### 2. 自定义配置
```json
{
  "game_settings": {
    "max_level": 20,
    "starting_gold": 100,
    "difficulty_multiplier": 1.0
  },
  "morality_settings": {
    "light_threshold": 8,
    "shadow_threshold": 8,
    "balance_threshold": 7
  }
}
```

## 📞 支持与反馈

### 技术支持
- **文档**: 查看game-materials目录中的详细材料
- **代码**: 参考shadow_throne_redemption.py核心逻辑
- **GUI**: 参考gui_game.py了解界面实现

### 问题反馈
如果遇到问题，请提供：
- Python版本
- 运行环境
- 错误信息
- 重现步骤

### 贡献指南
1. Fork项目
2. 创建功能分支
3. 提交代码
4. 发起Pull Request

---

《暗影王座的救赎》是一个完整的DND桌游项目，提供了从角色创建到最终结局的完整游戏体验。通过图形用户界面和GM工具包，玩家和GM都能获得良好的游戏体验。项目完全开源，可以根据需要进行扩展和定制。

## 📚 原始数据源 (仅用于数据参考)

本游戏基于DND JSON数据开发，原始数据来源于：

- **Player's Handbook, 2024 (PHB)**
- **Dungeon Master's Guide, 2024 (DMG)**
- **Monster Manual (MM)**
- **Xanathar's Guide to Everything (XGtE)**
- **Tasha's Cauldron of Everything (TCoE)**
- **Bigby Presents - Glory of the Giants**
- **Mordenkainen Presents - Monsters of the Multiverse**
- **Curse of Strahd**
- **Princes of the Apocalypse**

**注意**: 本游戏是一个完整的DND桌游实现，不仅仅是数据集合，而是包含了完整的游戏逻辑、GUI界面和GM工具包。
