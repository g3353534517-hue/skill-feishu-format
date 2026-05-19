# Feishu Message Format Enforcer / 飞书消息排版格式化器

![版本](https://img.shields.io/badge/版本-1.0.0-blue) ![分类](https://img.shields.io/badge/分类-效率工具-green)

## 项目简介

飞书消息排版强制技能。每次回复飞书用户时，发送前必须先调用脚本格式化输出，否则排版必崩。

飞书 post 模式的核心坑：单个换行符会被吞成空格，只有双换行才能真正分段。不调脚本就发消息 = 排版必崩。

## 飞书排版铁律

1. 禁止使用 `**加粗**`、`## 标题`、`--- 分割线`、`~~删除线~~`、`|表格|`、嵌套列表
2. 这些符号在飞书 post 模式下会裸露显示原始标记
3. 正确做法：用 emoji 做锚点、空行分段、· 列表、1.2.3. 步骤、短句化

## 分段规则

- ✅ 行间用单个换行符
- ✅ 板块标题前用两个换行符（空行）
- ❌ 禁止连续3个以上空行

## 使用方法

格式化消息（每次发飞书前必用）：

```bash
python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --fix "消息内容"
```

只检查不修改：

```bash
python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --check "消息内容"
```

通过标准输入传入：

```bash
echo "消息内容" | python3 ~/.hermes/skills/feishu-format/scripts/feishu_format.py --fix
```

## 文件结构

```
SKILL.md
_meta.json
scripts/feishu_format.py
```

## 许可证

MIT License
