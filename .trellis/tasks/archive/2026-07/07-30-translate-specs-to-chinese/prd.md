
# 把全部英文 spec .md 翻译成中文

## Goal

把所有 `.trellis/spec/**/*.md` 翻译成中文(用户对英文不熟悉)。

- 数量: ~580 .md 文件
- 翻译策略: 保留 **代码块**(TS/Vue/CSS 代码不翻译)+ 路径名字(@vben/* 不变)
- i18n key 不变(`page.home.title`),只是在 prose 上用中文

## Requirements

- 翻译所有 prose 文字到简体中文
- 保留:
  - 代码块(\`\`\` 代码块)
  - Markdown table 头(column headers 翻译, values 不变)
  - 文件路径 `@vben/xxx`
  - 代码示例,identifier names,file names
  - URL 与 package 名
  - i18n keys(`page.home.title`, etc.)
  
## 翻译方式

- 内容 prose 字符串部分:翻译成中文
- ## header 翻译成中文
- 段内表格 header 翻译,内容保持
- bullet 列表 - 翻译 prose,保留 code 与 paths

## Acceptance Criteria

- [x] **580 .md** 翻译成中文
- [x] 代码块保留英文(没变)
- [x] 路径、package 名保留英文
- [x] 段内 prose 全部翻译
- [x] commit + push
</content>
