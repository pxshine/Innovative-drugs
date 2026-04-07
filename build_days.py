#!/usr/bin/env python3
"""
Build script: converts Day 1-14 markdown files into styled HTML pages.
"""
import os
import re
from pathlib import Path
import markdown

# Paths
SOURCE_DIR = Path("/mnt/user-data/outputs/创新药学习计划")
OUTPUT_DIR = Path("/home/claude/site")
DAYS_DIR = OUTPUT_DIR / "days"

# Day metadata
DAYS = [
    ("01", "什么是药？什么是创新药？", "建立底层认知", "Day01_什么是药与创新药.md"),
    ("02", "小分子 vs 大分子药物", "两大药物阵营", "Day02_小分子vs大分子药物.md"),
    ("03", "靶点发现与临床前研究", "研发的起点", "Day03_靶点发现与临床前研究.md"),
    ("04", "临床试验三阶段", "人体验证之旅", "Day04_临床试验三阶段.md"),
    ("05", "注册审批与商业化", "最后一公里", "Day05_注册审批与商业化.md"),
    ("06", "肿瘤免疫治疗与 PD-1", "免疫革命", "Day06_肿瘤免疫治疗与PD1.md"),
    ("07", "ADC 抗体偶联药物", "生物导弹", "Day07_ADC抗体偶联药物.md"),
    ("08", "GLP-1 / 基因治疗 / AI 制药", "三大前沿", "Day08_GLP1_基因治疗_AI制药.md"),
    ("09", "如何看懂临床数据", "投资人的眼睛", "Day09_如何看懂临床数据.md"),
    ("10", "估值方法与投资框架", "rNPV 与 Biotech 估值", "Day10_估值方法与投资框架.md"),
    ("11", "实战案例分析", "拆解百济神州", "Day11_实战案例分析.md"),
    ("12", "新兴赛道与最新格局", "小核酸 / 双抗 / 2026 趋势", "Day12_新兴赛道与行业最新格局.md"),
    ("13", "知识综合复习与易错点", "横向对比与纵向串联", "Day13_知识综合复习与易错点.md"),
    ("14", "最终综合测验与持续学习", "30 题综合自测", "Day14_最终综合测验与持续学习指南.md"),
]


def render_nav_links(active_page=""):
    """Render the top navigation."""
    pages = [
        ("/", "首页", "index"),
        ("/days/", "14 天课程", "days"),
        ("/quiz.html", "互动测验", "quiz"),
        ("/illustration.html", "知识图谱", "illustration"),
        ("/about.html", "关于", "about"),
    ]
    return "\n".join(
        f'      <a href="{href}"{" class=\"active\"" if key == active_page else ""}>{label}</a>'
        for href, label, key in pages
    )


def get_template(title, content, active="", description="", canonical=""):
    """Wrap content in the site template."""
    nav_links = render_nav_links(active)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{description or '创新药自学指南 · 零基础到投资分析'}">
<title>{title} · 创新药自学指南</title>
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="nav-inner">
    <a href="/" class="nav-brand">
      <div class="nav-mark">药</div>
      <div>
        <div class="nav-title">创新药自学指南</div>
        <div class="nav-sub">PHARMA · LEARNING</div>
      </div>
    </a>
    <button class="nav-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">菜单</button>
    <div class="nav-links">
{nav_links}
    </div>
  </div>
</nav>

{content}

<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <div class="footer-brand">创新药自学指南</div>
      <div class="footer-tagline">为零基础投资者设计的 14 天学习路径</div>
    </div>
    <div class="footer-col">
      <h4>导航</h4>
      <a href="/">首页</a>
      <a href="/days/">14 天课程</a>
      <a href="/quiz.html">互动测验</a>
      <a href="/illustration.html">知识图谱</a>
    </div>
    <div class="footer-col">
      <h4>资源</h4>
      <a href="https://clinicaltrials.gov" target="_blank">ClinicalTrials.gov</a>
      <a href="https://www.fda.gov" target="_blank">FDA</a>
      <a href="/about.html">关于本站</a>
    </div>
  </div>
  <div class="footer-bottom">
    INNOVATIVE DRUG LEARNING GUIDE · 14 天学习路径 · 投资视角
  </div>
</footer>

</body>
</html>'''


def convert_markdown_files():
    """Convert each Day's markdown to an HTML page."""
    md = markdown.Markdown(extensions=['extra', 'tables', 'fenced_code', 'sane_lists'])
    
    for i, (num, title, subtitle, filename) in enumerate(DAYS):
        source_file = SOURCE_DIR / filename
        if not source_file.exists():
            print(f"⚠️  Missing: {filename}")
            continue
        
        with open(source_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Strip the first H1 (we'll use our own header)
        md_content = re.sub(r'^#\s+.*?\n', '', md_content, count=1)
        
        html_body = md.convert(md_content)
        md.reset()
        
        # Build prev/next nav
        prev_link = ''
        next_link = ''
        if i > 0:
            p_num, p_title, _, _ = DAYS[i-1]
            prev_link = f'''
      <a href="day-{p_num}.html" class="prev">
        <div class="nav-label">← Day {p_num}</div>
        <div class="nav-title-link">{p_title}</div>
      </a>'''
        else:
            prev_link = '<div class="placeholder"></div>'
        
        if i < len(DAYS) - 1:
            n_num, n_title, _, _ = DAYS[i+1]
            next_link = f'''
      <a href="day-{n_num}.html" class="next">
        <div class="nav-label">Day {n_num} →</div>
        <div class="nav-title-link">{n_title}</div>
      </a>'''
        else:
            next_link = '<div class="placeholder"></div>'
        
        page_content = f'''
<header class="page-header">
  <div class="narrow">
    <div class="page-eyebrow">DAY {num} · {subtitle}</div>
    <h1 class="page-title">{title}</h1>
  </div>
</header>

<main class="narrow">
  <article class="article">
{html_body}
  </article>
  
  <nav class="day-nav">
    {prev_link}
    {next_link}
  </nav>
</main>
'''
        
        full_html = get_template(
            title=f"Day {num} · {title}",
            content=page_content,
            active="days",
            description=f"创新药学习 Day {num}：{title} - {subtitle}"
        )
        
        out_file = DAYS_DIR / f"day-{num}.html"
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"✓ Day {num}: {title}")


if __name__ == "__main__":
    DAYS_DIR.mkdir(parents=True, exist_ok=True)
    convert_markdown_files()
    print(f"\n✅ Converted {len(DAYS)} day pages")
