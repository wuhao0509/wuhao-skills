#!/usr/bin/env python3
"""
Logseq 到 Obsidian 批量迁移脚本
支持自动分类、格式转换、预览模式
"""

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Optional


def load_category_mapping(skill_dir: Path) -> dict:
    """加载分类映射配置"""
    mapping_file = skill_dir.parent / "category_mapping.json"
    if mapping_file.exists():
        return json.loads(mapping_file.read_text(encoding='utf-8'))
    return {"category_mapping": {}, "default_folder": ""}


def get_target_folder(filename: str, category_mapping: dict) -> str:
    """根据文件名匹配目标文件夹"""
    # 移除开头的数字序号（如 "01 ", "02 "）
    clean_name = re.sub(r'^\d+\s+', '', filename)
    
    for category, config in category_mapping.get("category_mapping", {}).items():
        if config.get("is_journal"):
            continue
        keywords = config.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in clean_name.lower():
                return config.get("folder", "")
    
    return category_mapping.get("default_folder", "")


def convert_outline_to_markdown(content: str) -> str:
    """将 Logseq 大纲格式转为标准 Markdown"""
    lines = content.split('\n')
    result = []
    for line in lines:
        stripped = line.lstrip('\t')
        if stripped == '-' or stripped.strip() == '':
            continue
        if stripped.startswith('- '):
            rest = stripped[2:].strip()
            if not rest:
                continue
            # 检测标题
            m = re.match(r'^(#+)\s+(.+)$', rest)
            if m:
                level = len(m.group(1)) + 1
                heading = m.group(2).strip()
                result.append('#' * level + ' ' + heading)
            # 任务状态
            elif rest.startswith('TODO '):
                result.append(f'- [ ] {rest[5:]}')
            elif rest.startswith('DOING '):
                result.append(f'- [ ] {rest[6:]} #status/doing')
            elif rest.startswith('DONE '):
                result.append(f'- [x] {rest[5:]}')
            elif rest.startswith('LATER '):
                result.append(f'- [ ] {rest[6:]} #status/later')
            elif rest.startswith('WAITING '):
                result.append(f'- [ ] {rest[8:]} #status/waiting')
            else:
                result.append(stripped)
        else:
            result.append(line)
    return '\n'.join(result)


def convert_content(content: str, source_filename: str = '') -> str:
    """转换单文件内容"""
    # 移除 id:: 属性
    content = re.sub(r'\n\s+id:: [a-f0-9-]+(?:\s*\n|$)', '\n', content)
    content = re.sub(r'\n\s*id:: [a-f0-9-]+\s*$', '', content)
    # 移除高亮颜色标记
    content = re.sub(r'\[\[\$[a-zA-Z]+\]\]', '', content)
    # 日记链接格式转换
    content = re.sub(r'\[\[(\d{4})_(\d{2})_(\d{2})\]\]', r'[[\1-\2-\3]]', content)
    # 块引用转换
    page_name = Path(source_filename).stem if source_filename else 'page'
    content = re.sub(r'\(\(([a-f0-9-]+)\)\)', rf'[[{page_name}#^\1]]', content)
    # 资源路径转换
    content = content.replace('../assets/', 'assets/')
    # 大纲转换
    content = convert_outline_to_markdown(content)
    return content


def migrate_file(
    source_file: Path,
    target_dir: Path,
    category_mapping: dict,
    preview: bool = False
) -> tuple:
    """迁移单个文件，返回 (目标路径, 状态信息)"""
    # 确定目标文件夹
    target_folder = get_target_folder(source_file.name, category_mapping)
    
    if target_folder:
        target_subdir = target_dir / target_folder
    else:
        target_subdir = target_dir
    
    # 日记文件特殊处理
    if 'journals' in str(source_file):
        target_subdir = target_dir / '日记'
        # 重命名文件
        new_name = source_file.name.replace('_', '-')
        target_file = target_subdir / new_name
    else:
        target_file = target_subdir / source_file.name
    
    # 读取并转换内容
    content = source_file.read_text(encoding='utf-8')
    converted = convert_content(content, source_file.name)
    
    if preview:
        return str(target_file), f"[预览] 将迁移到: {target_file}"
    
    # 确保目标目录存在
    target_subdir.mkdir(parents=True, exist_ok=True)
    
    # 写入转换后的文件
    target_file.write_text(converted, encoding='utf-8')
    
    return str(target_file), f"OK: {target_file}"


def migrate_assets(source_dir: Path, target_dir: Path) -> int:
    """迁移 assets 目录"""
    source_assets = source_dir / 'assets'
    target_assets = target_dir / 'assets'
    
    if not source_assets.exists():
        return 0
    
    target_assets.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for file in source_assets.iterdir():
        if file.is_file():
            target_file = target_assets / file.name
            shutil.copy2(file, target_file)
            count += 1
    
    return count


def main():
    parser = argparse.ArgumentParser(description='Logseq 到 Obsidian 迁移工具')
    parser.add_argument('--source', required=True, help='Logseq 源仓库路径')
    parser.add_argument('--target', required=True, help='Obsidian 目标仓库路径')
    parser.add_argument('--file', help='仅迁移指定文件（预览模式）')
    parser.add_argument('--preview', action='store_true', help='预览模式，不实际写入文件')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，显示迁移计划')
    args = parser.parse_args()
    
    source_dir = Path(args.source)
    target_dir = Path(args.target)
    skill_dir = Path(__file__).parent
    
    # 加载分类配置
    category_mapping = load_category_mapping(skill_dir)
    
    print("=" * 60)
    print("Logseq -> Obsidian 迁移工具")
    print("=" * 60)
    print(f"源仓库: {source_dir}")
    print(f"目标仓库: {target_dir}")
    print()
    
    # 单文件预览模式
    if args.file:
        source_file = source_dir / args.file
        if not source_file.exists():
            print(f"错误: 文件不存在 {source_file}")
            return
        
        target_path, status = migrate_file(
            source_file, target_dir, category_mapping, preview=True
        )
        print(f"文件: {args.file}")
        print(f"状态: {status}")
        print()
        print("转换后内容:")
        print("-" * 40)
        print(convert_content(source_file.read_text(encoding='utf-8'), source_file.name))
        return
    
    # 统计信息
    stats = {
        'pages': 0,
        'journals': 0,
        'assets': 0,
        'by_folder': {}
    }
    
    # 模拟运行
    if args.dry_run or args.preview:
        print("[模拟运行] 迁移计划:")
        print()
        
        # Pages
        pages_dir = source_dir / 'pages'
        if pages_dir.exists():
            print("### Pages 迁移计划:")
            for file in sorted(pages_dir.glob('*.md')):
                folder = get_target_folder(file.name, category_mapping)
                target_path = target_dir / folder / file.name if folder else target_dir / file.name
                print(f"  {file.name} -> {target_path}")
                stats['pages'] += 1
                stats['by_folder'][folder or '根目录'] = stats['by_folder'].get(folder or '根目录', 0) + 1
        
        # Journals
        journals_dir = source_dir / 'journals'
        if journals_dir.exists():
            print()
            print("### Journals 迁移计划:")
            for file in sorted(journals_dir.glob('*.md'))[:5]:
                new_name = file.name.replace('_', '-')
                print(f"  {file.name} -> 日记/{new_name}")
            journal_count = len(list(journals_dir.glob('*.md')))
            if journal_count > 5:
                print(f"  ... 共 {journal_count} 个日记文件")
            stats['journals'] = journal_count
        
        # Assets
        assets_dir = source_dir / 'assets'
        if assets_dir.exists():
            stats['assets'] = len(list(assets_dir.iterdir()))
        
        print()
        print("### 分类统计:")
        for folder, count in sorted(stats['by_folder'].items()):
            print(f"  {folder}: {count} 个文件")
        
        print()
        print(f"总计: Pages {stats['pages']}, Journals {stats['journals']}, Assets {stats['assets']}")
        return
    
    # 实际迁移
    print("开始迁移...")
    print()
    
    # 迁移 assets
    asset_count = migrate_assets(source_dir, target_dir)
    print(f"Assets: 已迁移 {asset_count} 个文件")
    
    # 迁移 pages
    pages_dir = source_dir / 'pages'
    if pages_dir.exists():
        for file in pages_dir.glob('*.md'):
            try:
                target_path, status = migrate_file(
                    file, target_dir, category_mapping
                )
                print(status)
                stats['pages'] += 1
            except Exception as e:
                print(f"ERROR: {file.name} - {e}")
    
    # 迁移 journals
    journals_dir = source_dir / 'journals'
    if journals_dir.exists():
        for file in journals_dir.glob('*.md'):
            try:
                target_path, status = migrate_file(
                    file, target_dir, category_mapping
                )
                print(status)
                stats['journals'] += 1
            except Exception as e:
                print(f"ERROR: {file.name} - {e}")
    
    print()
    print("=" * 60)
    print("迁移完成!")
    print(f"Pages: {stats['pages']}")
    print(f"Journals: {stats['journals']}")
    print(f"Assets: {asset_count}")
    print("=" * 60)


if __name__ == '__main__':
    main()