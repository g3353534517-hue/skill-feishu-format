#!/usr/bin/env python3
"""
飞书消息排版检查 + 自动修复

拆分策略（层层递进，每层拆完对子行递归）：
 1. 按·列表项拆（前缀递归拆）
 2. 按数字emoji编号 1️⃣2️⃣3️⃣ 拆
 3. 按普通数字编号 1. 2. 3. 拆
 4. 按行中emoji板块标记拆
 5. 长段落按句号拆

关键：前缀拆分时force=True，跳过长度检查

用法：
 python3 feishu_format.py "消息"
 python3 feishu_format.py --check "消息"
 python3 feishu_format.py --fix "消息"
 echo "消息" | python3 feishu_format.py --fix
"""

import re
import sys

MAX_LINE_LENGTH = 60

BANNED_PATTERNS = [
    (r'\*\*[^*]+\*\*', "星号加粗 **text**"),
    (r'^\s*#{1,6}\s', "井号标题 # "),
    (r'^-{3,}$', "分割线 ---"),
    (r'^\*{3,}$', "分割线 ***"),
    (r'~~[^~]+~~', "删除线 ~~text~~"),
    (r'\|.*\|.*\|', "Markdown表格 |...|"),
]

EMOJI_HEADING_RE = re.compile(
    r'^[\U0001F300-\U0001F9FF\U00002702-\U000027B0'
    r'\U0001FA00-\U0001FAFF\U00002600-\U000026FF'
    r'\U00002700-\U000027BF\U0001F900-\U0001F9FF]'
)


def check(text):
    violations = []
    lines = text.split('\n')
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        for pattern, desc in BANNED_PATTERNS:
            if re.search(pattern, s):
                for m in re.findall(pattern, s):
                    violations.append((i, desc, m[:60]))
                break
        if len(s) > MAX_LINE_LENGTH and not s.startswith(('http', 'https')):
            violations.append((i, f"行过长({len(s)}字)", s[:50] + "..."))
    for i, line in enumerate(lines):
        s = line.strip()
        if s and EMOJI_HEADING_RE.match(s):
            if i > 0 and lines[i - 1].strip() != '':
                violations.append((i + 1, "emoji标题前缺空行", s[:40]))
    return violations


def fix(text):
    # 去违规符号
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'(^\s*|\s)#{2,6}[\s]?', r'\1', text)  # #标题（2个#以上），保留C#等单#
    text = re.sub(r'^-{3,}$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\*{3,}$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    text = re.sub(r'^\|.*\|.*\|$\n?', '', text, flags=re.MULTILINE)

    # 逐行拆分
    lines = text.split('\n')
    expanded = []
    for line in lines:
        s = line.strip()
        if not s:
            expanded.append('')
            continue
        expanded.extend(_smart_split(s, depth=0))

    # 补空行：emoji标题前补空行（但打卡项✅❌之间不加空行）
    result = []
    for line in expanded:
        s = line.strip()
        if not s:
            result.append('')
            continue
        if EMOJI_HEADING_RE.match(s):
            if result and result[-1] != '':
                # ✅❌开头的是打卡项，之间不加空行
                if not (s.startswith(('✅', '❌', '⚠️📝')) or
                        (result[-1].startswith(('✅', '❌')) and EMOJI_HEADING_RE.match(s))):
                    result.append('')
        result.append(s)

    # 清理连续空行
    text = '\n'.join(result)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def _smart_split(line, depth=0, force=False):
    """智能拆行。force=True时跳过长度检查，强制尝试所有拆分策略"""
    if depth > 5:
        return [line]

    s = line.strip()
    if not s:
        return []

    # 非force模式下，短行直接返回
    if not force and len(s) <= MAX_LINE_LENGTH:
        return [s]

    # ── 策略1：按·列表项拆 ──
    if '· ' in s:
        first_dot = s.find('· ')
        prefix = s[:first_dot].strip()
        body = s[first_dot:]

        dot_parts = re.split(r'(?=· )', body)
        dot_parts = [p.strip() for p in dot_parts if p.strip()]

        result = []
        if prefix:
            # prefix强制递归拆（不管多短，可能含emoji标题+编号）
            result.extend(_smart_split(prefix, depth + 1, force=True))
        # 每个dot_part也递归检查（可能含keycap/emoji需要继续拆）
        for dp in dot_parts:
            result.extend(_smart_split(dp, depth + 1, force=True))
        if len(result) > 1:
            return result

    # ── 策略2：按数字emoji编号 1️⃣2️⃣3️⃣ 拆 ──
    keycap_pattern = r'[1-9]\ufe0f\u20e3|[1-9]\u20e3'
    positions = [m.start() for m in re.finditer(keycap_pattern, s)]
    if len(positions) >= 1:
        parts = []
        prev = 0
        for pos in positions:
            part = s[prev:pos].strip()
            if part:
                parts.append(part)
            prev = pos
        last = s[prev:].strip()
        if last:
            parts.append(last)
        if len(parts) > 1:
            # 对每个子段递归拆（子段可能还有·列表项）
            result = []
            for p in parts:
                result.extend(_smart_split(p, depth + 1, force=False))
            return result

    # ── 策略3：按普通数字编号 1. 2. 3. 拆 ──
    num_splits = re.split(r'(?=[1-9][\.\)、]\s)', s)
    num_splits = [p.strip() for p in num_splits if p.strip()]
    if len(num_splits) > 1:
        result = []
        for p in num_splits:
            result.extend(_smart_split(p, depth + 1))
        return result

    # ── 策略4：按行中emoji板块标记拆 ──
    # 匹配：中文/右括号/空格 紧跟 emoji（非行首）
    pattern = (
        r'(?<=[\u4e00-\u9fff\)\）\s])'
        r'(?=[\U0001F300-\U0001F9FF\U00002702-\U000027B0'
        r'\U0001FA00-\U0001FAFF\U00002600-\U000026FF'
        r'\U00002700-\U000027BF\U0001F900-\U0001F9FF])'
    )
    emoji_positions = [m.start() for m in re.finditer(pattern, s)]
    if emoji_positions:
        parts = []
        prev = 0
        for pos in emoji_positions:
            part = s[prev:pos].strip()
            if part:
                parts.append(part)
            prev = pos
        last = s[prev:].strip()
        if last:
            parts.append(last)
        if len(parts) > 1:
            result = []
            for p in parts:
                result.extend(_smart_split(p, depth + 1))
            return result

    # ── 策略5：长段落按句号拆 ──
    if '。' in s and len(s) > MAX_LINE_LENGTH * 1.5:
        sent = re.split(r'(?<=。)\s*', s)
        sent = [p.strip() for p in sent if p.strip()]
        if len(sent) > 1:
            return sent

    return [s]


def report_violations(violations):
    if not violations:
        return ""
    lines = [f"❌ 发现{len(violations)}个排版问题：", ""]
    seen = set()
    for line_no, desc, original in violations:
        key = (desc, original)
        if key not in seen:
            seen.add(key)
            lines.append(f"  第{line_no}行 [{desc}] → {original}")
    return "\n".join(lines)


if __name__ == "__main__":
    mode = "both"
    text = ""
    args = sys.argv[1:]

    if "--check" in args:
        mode = "check"
        args.remove("--check")
    elif "--fix" in args:
        mode = "fix"
        args.remove("--fix")

    if args:
        text = " ".join(args)
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("用法: python3 feishu_format.py [--check|--fix] '消息内容'")
        sys.exit(1)

    violations = check(text)
    fixed = fix(text)
    changed = fixed != text

    if mode == "check":
        r = report_violations(violations)
        print(r if r else "✅ 排版检查通过")
        sys.exit(0 if not violations else 1)
    elif mode == "fix":
        print(fixed)
    else:
        r = report_violations(violations)
        if r:
            print(r)
            print()
        if changed:
            if not r:
                print("⚠️ 换行需要规范化")
                print()
            print("👇 修复后：")
            print()
            print(fixed)
        elif r:
            print("⚠️ 有违规符号需手动处理")
        else:
            print("✅ 排版检查通过")

    sys.exit(0)
