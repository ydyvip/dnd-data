#!/usr/bin/env python3
"""
测试JSON数据加载功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shadow_throne_redemption import Game

def test_json_loading():
    """测试JSON数据加载功能"""
    print("🧪 测试JSON数据加载功能...")
    
    # 创建游戏实例
    game = Game()
    
    # 测试背景数据加载
    print(f"\n📋 背景数据测试:")
    print(f"   JSON背景数量: {len(game.backgrounds)}")
    print(f"   前5个背景: {game.backgrounds[:5]}")
    
    # 测试职业数据加载
    print(f"\n⚔️ 职业数据测试:")
    print(f"   JSON职业数量: {len(game.character_classes)}")
    print(f"   前5个职业: {game.character_classes[:5]}")
    
    # 测试装备数据加载
    print(f"\n🛡️ 装备数据测试:")
    print(f"   JSON装备数量: {len(game.equipment_database)}")
    print(f"   前5个装备: {[eq.name for eq in game.equipment_database[:5]]}")
    
    # 测试法术数据加载
    print(f"\n✨ 法术数据测试:")
    print(f"   JSON法术数量: {len(game.spell_database)}")
    print(f"   前5个法术: {[spell.name for spell in game.spell_database[:5]]}")
    
    # 测试怪物数据加载
    print(f"\n👹 怪物数据测试:")
    print(f"   JSON怪物数量: {len(game.monster_database)}")
    print(f"   前5个怪物: {[monster.name for monster in game.monster_database[:5]]}")
    
    # 测试数据完整性
    print(f"\n🔍 数据完整性检查:")
    success_count = 0
    
    # 检查背景数据
    if game.backgrounds and len(game.backgrounds) > 0:
        print("   ✅ 背景数据加载成功")
        success_count += 1
    else:
        print("   ❌ 背景数据加载失败")
    
    # 检查职业数据
    if game.character_classes and len(game.character_classes) > 0:
        print("   ✅ 职业数据加载成功")
        success_count += 1
    else:
        print("   ❌ 职业数据加载失败")
    
    # 检查装备数据
    if game.equipment_database and len(game.equipment_database) > 0:
        print("   ✅ 装备数据加载成功")
        success_count += 1
    else:
        print("   ❌ 装备数据加载失败")
    
    # 检查法术数据
    if game.spell_database and len(game.spell_database) > 0:
        print("   ✅ 法术数据加载成功")
        success_count += 1
    else:
        print("   ❌ 法术数据加载失败")
    
    # 检查怪物数据
    if game.monster_database and len(game.monster_database) > 0:
        print("   ✅ 怪物数据加载成功")
        success_count += 1
    else:
        print("   ❌ 怪物数据加载失败")
    
    print(f"\n📊 测试结果: {success_count}/5 项数据加载成功")
    
    if success_count == 5:
        print("🎉 所有JSON数据加载测试通过！")
        return True
    else:
        print("⚠️ 部分数据加载失败，请检查JSON文件路径和格式")
        return False

if __name__ == "__main__":
    test_json_loading()