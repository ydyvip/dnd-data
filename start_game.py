#!/usr/bin/env python3
"""
《暗影王座的救赎》游戏启动脚本
一键启动游戏的入口脚本
"""

import subprocess
import sys
import os

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误：需要Python 3.7或更高版本")
        print(f"当前版本：Python {sys.version}")
        return False
    return True

def check_dependencies():
    """检查依赖"""
    try:
        import tkinter
        return True
    except ImportError:
        print("❌ 错误：缺少Tkinter库")
        print("请确保Python安装时包含了Tkinter组件")
        return False

def show_menu():
    """显示启动菜单"""
    print("🎮 《暗影王座的救赎》DND游戏")
    print("=" * 40)
    print("请选择启动方式：")
    print("1. 控制台版本（文本界面）")
    print("2. 图形界面版本（推荐）")
    print("3. GM工具包")
    print("4. 运行测试")
    print("5. 查看项目文档")
    print("6. 退出")
    print("=" * 40)

def launch_console_game():
    """启动控制台版本"""
    print("🚀 启动控制台版本...")
    try:
        subprocess.run([sys.executable, "shadow_throne_redemption.py"])
    except KeyboardInterrupt:
        print("\n游戏已退出")
    except Exception as e:
        print(f"❌ 启动失败：{e}")

def launch_gui_game():
    """启动图形界面版本"""
    print("🚀 启动图形界面版本...")
    try:
        subprocess.run([sys.executable, "gui_game.py"])
    except KeyboardInterrupt:
        print("\n游戏已退出")
    except Exception as e:
        print(f"❌ 启动失败：{e}")

def launch_gm_tools():
    """启动GM工具包"""
    print("🚀 启动GM工具包...")
    try:
        subprocess.run([sys.executable, "gm_tools.py"])
    except KeyboardInterrupt:
        print("\nGM工具包已退出")
    except Exception as e:
        print(f"❌ 启动失败：{e}")

def run_tests():
    """运行测试"""
    print("🧪 运行游戏测试...")
    try:
        # 运行单元测试
        subprocess.run([sys.executable, "-m", "unittest", "test_game.py"], 
                     cwd=os.path.dirname(os.path.abspath(__file__)))
        print("✅ 测试完成")
    except Exception as e:
        print(f"❌ 测试失败：{e}")

def show_documentation():
    """显示文档"""
    print("📖 显示项目文档...")
    print("\n" + "="*60)
    print("《暗影王座的救赎》DND游戏项目文档")
    print("="*60)
    
    print("\n🎮 游戏特色：")
    print("- 三维道德系统：光明、暗影、平衡值影响结局")
    print("- 四章节剧情：1-20级的完整成长体验")
    print("- 三种结局：光明救赎、黑暗统治、平衡之道")
    print("- 丰富的角色选择：405种背景，134种职业")
    
    print("\n📁 项目结构：")
    print("- shadow_throne_redemption.py: 游戏核心引擎")
    print("- gui_game.py: 图形用户界面")
    print("- gm_tools.py: GM工具包")
    print("- game-materials/: 游戏材料目录")
    
    print("\n🚀 启动方式：")
    print("- 控制台版本: python shadow_throne_redemption.py")
    print("- 图形界面版本: python gui_game.py")
    print("- GM工具包: python gm_tools.py")
    
    print("\n📋 游戏规则：")
    print("- 角色创建：选择背景、职业，设置初始属性")
    print("- 战斗系统：回合制战斗，包含攻击、法术、技能")
    print("- 道德选择：每个选择都影响最终结局")
    print("- 任务系统：接受任务，完成挑战，获得奖励")
    print("- 成长系统：获得经验值，提升等级，学习技能")
    
    print("\n🎯 GM功能：")
    print("- NPC关系追踪：管理NPC与玩家的关系")
    print("- 战斗难度计算：计算战斗难度和平衡性")
    print("- 随机事件生成：生成即兴游戏事件")
    print("- 剧情生成器：生成紧急剧情线")
    print("- 世界构建工具：构建游戏世界观")
    
    print("\n📊 游戏数据：")
    print("- 背景选项: 405种")
    print("- 职业选择: 134种")
    print("- 怪物数量: 11,463种")
    print("- 装备道具: 15,749种")
    print("- 法术数量: 5,849种")
    print("- 章节数量: 4个")
    print("- 结局数量: 3种")
    
    print("\n🔧 扩展功能：")
    print("- 添加新的职业和背景")
    print("- 自定义法术和技能")
    print("- 创建新的游戏模组")
    print("- 网络多人游戏支持")
    
    print("\n📞 支持与反馈：")
    print("- 如有问题，请查看README.md")
    print("- 欢迎贡献代码和改进建议")
    
    print("\n" + "="*60)

def main():
    """主函数"""
    print("🎮 《暗影王座的救赎》启动器")
    print("="*40)
    
    # 检查环境
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        print("💡 提示：如果无法启动图形界面，请尝试控制台版本")
    
    while True:
        show_menu()
        
        try:
            choice = input("请输入选择 (1-6): ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 感谢使用《暗影王座的救赎》！")
            break
        
        if choice == "1":
            launch_console_game()
        elif choice == "2":
            launch_gui_game()
        elif choice == "3":
            launch_gm_tools()
        elif choice == "4":
            run_tests()
        elif choice == "5":
            show_documentation()
        elif choice == "6":
            print("👋 感谢使用《暗影王座的救赎》！")
            break
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按Enter键继续...")

if __name__ == "__main__":
    main()