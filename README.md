# Feishu Message Format Enforcer / 飞书消息排版格式化器

![分类](https://img.shields.io/badge/分类-效率工具-green)

## 项目简介

飞书消息排版强制技能。每次回复飞书用户时，发送前必须先调用脚本格式化输出。飞书 post 模式下单个换行会被吞成空格，只有双换行才能真正分段。不调用脚本就发消息=排版必崩。

## 功能特性

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
- stdin

## 使用示例

```bash
# 格式化（你每次都要用这个）
python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --fix "消息"

# 只检查
python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --check "消息"

# stdin
echo "消息" | python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --fix
```

## 文件结构

```
SKILL.md
_meta.json
scripts/feishu_format.py
```

## 许可证

MIT License

---

更多项目请访问：[github.com/g3353534517-hue?tab=repositories](https://github.com/g3353534517-hue?tab=repositories)
