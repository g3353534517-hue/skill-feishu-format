# 飞书消息排版格式化 / Feishu Message Format Enforcer

![分类](https://img.shields.io/badge/分类-feishu--format-green)

## 简介 / Overview

飞书消息排版强制技能。每次回复飞书用户时，在发送最终消息之前，必须先调用脚本格式化输出。这不是可选的，是强制的。不调用就发消息=排版必崩。

## 详细说明 / Details

## 永久最高优先级铁律（没有例外）

飞书 post 模式下，单个 \n 会被合并成空格，只有 \n\n（空行）才能真正分段。

每次给飞书用户发消息，必须严格执行以下流程：

1. 写好消息内容
2. 跑 python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --fix "消息"
3. 拿到脚本输出后，确保板块间用 \n\n 分段
4. 最终检查：标题/板块前是否有 \n\n，✅❌行间是否只用 \n
5. 这个输出才是最终发送内容

直接发原始内容=违规。跑完脚本不用脚本输出=违规。偷懒跳过=违规。
用单个 \n 做段落分隔=违规。板块前没加 \n\n=违规。
⚠️ 跑完脚本后手动二次加工=违规。脚本输出即最终内容，一字不改直接发。

## 禁止的符号（用了就会裸露显示）

1. 星号加粗 **text** → 飞书会显示原始星号
2. 井号标题 ## 标题 → 飞书会显示原始##
3. 分割线 --- → 飞书会显示原始---
4. 删除线 ~~text~~ → 飞书会显示原始~~
5. Markdown表格 |...| → 飞书不支持
6. 嵌套列表缩进 → 飞书不支持

## 分行规则

1. \n\n 才是段落分隔（单个 \n 会被吞成空格）
2. emoji标题行前必须 \n\n
3. 列表项·每项独占一行（\n）
4. 数字编号1️⃣2️⃣3️⃣每项独占一行（\n）
5. ✅❌打卡行之间用 \n，板块标题前用 \n\n
6. 单行不超60字
7. 禁止连续3+个 \n\n

## 正确做法

· emoji代替标题
· \n\n 空行分隔段落/板块
· ·连接并列要点
· 1. 2. 3.列步骤
· 纯文本+emoji，不依赖任何markdown

## 正例

标题：今日总结\n\n...

## 功能特性 / Features

- 飞书排版强制技能
- 永久最高优先级铁律（没有例外）
- 禁止的符号（用了就会裸露显示）
- 分行规则
- 正确做法
- 正例
- 反例（永远禁止）
- 脚本用法
- 格式化（你每次都要用这个）
- 只检查

## 使用示例 / Usage Examples

```bash
# 格式化（你每次都要用这个）
python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --fix "消息"

# 只检查
python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --check "消息"

# stdin
echo "消息" | python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --fix
```

## 文件结构 / File Structure

```
SKILL.md
_meta.json
scripts/feishu_format.py
```

## 作者 / Author

Hermes Agent Community

## 许可证 / License

MIT License

---

更多技能请访问：[github.com/g3353534517-hue?tab=repositories](https://github.com/g3353534517-hue?tab=repositories)
