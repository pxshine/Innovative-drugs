# 创新药自学指南 · 静态站点

一套完整的创新药学习静态网站，包含 14 天课程、互动测验、知识图谱与首页概览。

## 📁 目录结构

```
site/
├── index.html              # 首页（概览 + 14 天卡片网格）
├── about.html              # 关于本站
├── quiz.html               # 互动测验（5 题）
├── illustration.html       # 知识图谱（彩色 SVG）
├── days/
│   ├── index.html          # 14 天课程目录页
│   ├── day-01.html         # Day 01 - 14
│   ├── day-02.html
│   ├── ...
│   └── day-14.html
├── assets/
│   └── style.css           # 共享样式表
└── README.md               # 本文档
```

## 🎨 设计风格

**编辑杂志风（Editorial Magazine）**
- **配色**：奶白米色背景（#f5f1e8）+ 深炭灰文字 + 酒红色（#8b1e1e）作为强调
- **字体**：Noto Serif SC（衬线大标题）+ Inter（无衬线正文）+ JetBrains Mono（标签）
- **特点**：大量留白、克制的色彩运用、长文阅读友好、适合作为知识库长期使用

## 🚀 部署到远程服务器

### 方式一：直接通过 rsync 部署

```bash
# 假设你的服务器是 user@your-server.com，目标目录是 /var/www/innovative-drug
rsync -avz --delete ./site/ user@your-server.com:/var/www/innovative-drug/
```

### 方式二：通过 scp 上传

```bash
# 打包后上传
tar -czf site.tar.gz site/
scp site.tar.gz user@your-server.com:/tmp/
ssh user@your-server.com 'cd /var/www && tar -xzf /tmp/site.tar.gz && rm /tmp/site.tar.gz'
```

### 方式三：通过 git（推荐）

```bash
# 在服务器上
cd /var/www
git clone <your-repo-url> innovative-drug
# 后续更新
cd innovative-drug && git pull
```

## 🔧 Nginx 配置

将以下配置保存为 `/etc/nginx/sites-available/innovative-drug.conf`：

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com www.your-domain.com;

    root /var/www/innovative-drug;
    index index.html;

    # 启用 gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/json
        application/xml
        image/svg+xml;

    # 静态资源缓存
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # HTML 文件不强缓存（方便更新）
    location ~* \.html$ {
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }

    # 主路由：尝试静态文件 → 目录 index → 404
    location / {
        try_files $uri $uri/ $uri.html =404;
    }

    # 隐藏 .html 后缀（可选，更优雅的 URL）
    # 访问 /days/day-01 等同于 /days/day-01.html
    location ~ ^/(.+)$ {
        try_files /$1.html /$1/index.html /$1 =404;
    }

    # 错误页面
    error_page 404 /404.html;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/innovative-drug.conf /etc/nginx/sites-enabled/
sudo nginx -t                # 测试配置
sudo systemctl reload nginx  # 重新加载
```

## 🔒 添加 HTTPS（推荐）

使用 [Let's Encrypt](https://letsencrypt.org/) 免费证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

证书会自动续期。

## 🐳 使用 Docker 部署（可选）

创建 `Dockerfile`：

```dockerfile
FROM nginx:alpine
COPY ./site /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

构建与运行：

```bash
docker build -t innovative-drug-site .
docker run -d -p 80:80 --name drug-site innovative-drug-site
```

## 📦 使用其他静态托管服务

本站点是<strong>纯静态</strong>的，无任何后端依赖，可直接部署到：

- **Vercel**：`vercel deploy` 即可
- **Netlify**：拖拽 `site/` 文件夹到面板
- **GitHub Pages**：推送到 `gh-pages` 分支
- **Cloudflare Pages**：连接 Git 仓库自动部署
- **阿里云 OSS / 腾讯云 COS**：开启静态网站功能后上传

## 🛠 本地预览

任何静态文件服务器都可以：

```bash
# Python 内置（最简单）
cd site
python3 -m http.server 8000
# 访问 http://localhost:8000

# Node.js
npx serve site

# PHP
cd site && php -S localhost:8000
```

## 📝 内容更新流程

如果你修改了 Day 1-14 的 markdown 源文件，运行构建脚本重新生成：

```bash
python3 build_days.py
```

然后重新部署即可。

## ⚙️ 技术栈

- **纯静态 HTML/CSS/JavaScript**，无构建依赖
- **响应式设计**，移动端友好
- **无第三方追踪**，注重隐私
- **可访问性**：语义化 HTML、键盘可导航
- **加载速度**：单页平均 < 50KB（不含 Web 字体）

## 📄 许可

学习内容：仅供个人学习使用。
代码模板：MIT License。

---

**如有问题或建议**，欢迎反馈。祝学习顺利！
