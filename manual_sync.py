#!/usr/bin/env python3
"""
手动同步上游仓库的Python脚本
使用方法: python manual_sync.py
"""

import subprocess
import sys

def run_command(cmd, description):
    """运行命令并处理错误"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败")
        print(f"错误输出: {e.stderr}")
        return False

def main():
    print("🔄 开始手动同步上游仓库")
    print("=" * 50)
    
    # 1. 添加上游远程
    if not run_command(
        "git remote add upstream https://github.com/cmliu/edgetunnel.git 2>/dev/null || true",
        "添加上游远程"
    ):
        return False
    
    # 2. 获取上游更新
    if not run_command("git fetch upstream", "获取上游更新"):
        return False
    
    # 3. 检查是否有更新
    check_cmd = "git diff --quiet HEAD upstream/main"
    try:
        subprocess.run(check_cmd, shell=True, check=True)
        print("✅ 当前已是最新版本，无需同步")
        return True
    except subprocess.CalledProcessError:
        print("🔄 检测到更新，开始合并...")
    
    # 4. 合并更新
    if not run_command("git merge upstream/main", "合并上游更新"):
        return False
    
    # 5. 推送到origin
    if not run_command("git push origin main", "推送到当前仓库"):
        return False
    
    print("=" * 50)
    print("🎉 同步完成！")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)