<div align="center">

# 🔰 DevGuardian

**Intelligent Development Environment Resource Monitor & AI Diagnostic Engine**

**轻量级开发环境资源智能监控与AI诊断引擎**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-✓-brightgreen.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

**DevGuardian** is an intelligent development environment resource monitoring and AI diagnostic engine designed specifically for developers. Unlike traditional system monitors, DevGuardian focuses on **development tool chains**, intelligently identifying and monitoring development-related processes, providing AI-powered diagnostics and optimization suggestions.

**Inspiration**: While tools like htop and btop are excellent general-purpose monitors, they don't understand the unique needs of developers. DevGuardian bridges this gap by recognizing development tools (IDEs, build systems, browsers, AI coding assistants) and providing contextual insights.

### ✨ Core Features

- 🔍 **Smart Process Detection** - Automatically identifies development tools (VS Code, Cursor, Docker, Node.js, Python, etc.)
- 📊 **Real-time TUI Dashboard** - Beautiful terminal interface with color-coded metrics and progress bars
- 🧠 **AI Diagnostics Engine** - 8 built-in diagnostic rules for detecting resource issues and optimization opportunities
- 📈 **Trend Analysis** - Tracks CPU, memory, and disk usage trends over time
- 🎯 **Process Categorization** - Groups processes by type: editors, browsers, build tools, containers, etc.
- 💡 **Optimization Reports** - Generates actionable recommendations for improving development environment performance
- 🚀 **Zero Dependencies** - Only requires `psutil`, pure Python implementation
- 🖥️ **Cross-Platform** - Works on Linux, macOS, and Windows

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- psutil library

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/DevGuardian.git
cd DevGuardian

# Install dependencies
pip install -r requirements.txt

# Or install to system
pip install -e .
```

#### Usage

```bash
# Start interactive monitoring
python devguardian.py

# Generate optimization report
python devguardian.py --report

# Save report to file
python devguardian.py --report -o report.txt

# Set custom refresh interval (seconds)
python devguardian.py --interval 5

# Show help
python devguardian.py --help
```

### 📖 Detailed Usage Guide

#### Interactive Mode

When running in interactive mode, DevGuardian displays:

1. **System Metrics Panel** - Real-time CPU, memory, and disk usage with visual progress bars
2. **Top Processes List** - Development processes sorted by memory usage
3. **AI Diagnostics Panel** - Context-aware warnings and suggestions
4. **Trend Indicators** - Rising/falling/stable indicators for each metric

**Keyboard Controls:**
- Press `Ctrl+C` to exit

#### Process Categories

DevGuardian automatically categorizes processes:

| Category | Examples |
|----------|----------|
| editor | VS Code, Cursor, PyCharm, Vim, Neovim |
| browser | Chrome, Firefox, Edge, Electron apps |
| build | Webpack, Vite, TSC, Babel |
| test | Jest, Pytest, Cypress |
| lint | ESLint, Prettier, Black |
| container | Docker, Kubernetes, Podman |
| language | Python, Node.js, Rust, Go |
| ai_coding | Claude, Codex, Copilot, Cursor |

#### AI Diagnostics Rules

| Rule ID | Trigger Condition | Severity |
|---------|------------------|----------|
| high_cpu | CPU > 80% | warning |
| high_memory | Memory > 85% | critical |
| high_disk | Disk > 90% | critical |
| memory_leak_suspected | Rising memory trend + high usage | warning |
| browser_tabs_overload | Multiple browsers + high memory | info |
| dev_tools_overload | >15 dev processes | info |
| low_resources_for_build | High usage during build | warning |
| thermal_throttling_risk | CPU > 90% and rising | critical |

### 💡 Design Philosophy

DevGuardian was built with these principles:

1. **Developer-First** - Understands the development workflow and toolchain
2. **Actionable Insights** - Not just data, but meaningful recommendations
3. **Lightweight** - Minimal resource footprint, fast startup
4. **Extensible** - Easy to add new diagnostic rules and categories

### 📦 Packaging & Deployment

#### Using Makefile

```bash
# Install to system
make install

# Run directly
make run

# Generate report
make report

# Clean build artifacts
make clean
```

#### Standalone Script

DevGuardian is a single Python file that can be run directly:

```bash
chmod +x devguardian.py
./devguardian.py
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**DevGuardian（开发守护者）** 是一款专为开发者打造的智能开发环境资源监控与AI诊断引擎。与传统系统监控工具不同，DevGuardian专注于**开发工具链**，智能识别并监控与开发相关的进程，提供AI驱动的诊断和优化建议。

**灵感来源**：虽然 htop 和 btop 等工具是优秀的通用监控器，但它们并不理解开发者的独特需求。DevGuardian 通过识别开发工具（IDE、构建系统、浏览器、AI 编程助手）并提供上下文洞察来填补这一空白。

### ✨ 核心特性

- 🔍 **智能进程检测** - 自动识别开发工具（VS Code、Cursor、Docker、Node.js、Python 等）
- 📊 **实时 TUI 仪表盘** - 精美的终端界面，带颜色编码的指标和进度条
- 🧠 **AI 诊断引擎** - 8 条内置诊断规则，检测资源问题和优化机会
- 📈 **趋势分析** - 跟踪 CPU、内存和磁盘使用趋势
- 🎯 **进程分类** - 按类型分组进程：编辑器、浏览器、构建工具、容器等
- 💡 **优化报告** - 生成可操作的改进建议
- 🚀 **零依赖** - 仅需 `psutil`，纯 Python 实现
- 🖥️ **跨平台** - 支持 Linux、macOS 和 Windows

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- psutil 库

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DevGuardian.git
cd DevGuardian

# 安装依赖
pip install -r requirements.txt

# 或安装到系统
pip install -e .
```

#### 使用

```bash
# 启动交互式监控
python devguardian.py

# 生成优化报告
python devguardian.py --report

# 保存报告到文件
python devguardian.py --report -o report.txt

# 设置自定义刷新间隔（秒）
python devguardian.py --interval 5

# 显示帮助
python devguardian.py --help
```

### 📖 详细使用指南

#### 交互模式

在交互模式下，DevGuardian 显示：

1. **系统指标面板** - 实时 CPU、内存和磁盘使用率，带可视化进度条
2. **热门进程列表** - 按内存使用率排序的开发进程
3. **AI 诊断面板** - 上下文感知的警告和建议
4. **趋势指示器** - 每个指标的上升/下降/稳定指示

**键盘控制：**
- 按 `Ctrl+C` 退出

#### 进程分类

DevGuardian 自动对进程进行分类：

| 分类 | 示例 |
|------|------|
| editor | VS Code、Cursor、PyCharm、Vim、Neovim |
| browser | Chrome、Firefox、Edge、Electron 应用 |
| build | Webpack、Vite、TSC、Babel |
| test | Jest、Pytest、Cypress |
| lint | ESLint、Prettier、Black |
| container | Docker、Kubernetes、Podman |
| language | Python、Node.js、Rust、Go |
| ai_coding | Claude、Codex、Copilot、Cursor |

#### AI 诊断规则

| 规则 ID | 触发条件 | 严重级别 |
|---------|----------|----------|
| high_cpu | CPU > 80% | warning |
| high_memory | 内存 > 85% | critical |
| high_disk | 磁盘 > 90% | critical |
| memory_leak_suspected | 内存上升趋势 + 高使用率 | warning |
| browser_tabs_overload | 多浏览器 + 高内存 | info |
| dev_tools_overload | >15 个开发进程 | info |
| low_resources_for_build | 构建期间资源不足 | warning |
| thermal_throttling_risk | CPU > 90% 且上升 | critical |

### 💡 设计理念

DevGuardian 遵循以下原则构建：

1. **开发者优先** - 理解开发工作流和工具链
2. **可操作的洞察** - 不只是数据，而是有意义的建议
3. **轻量级** - 最小资源占用，快速启动
4. **可扩展** - 易于添加新的诊断规则和分类

### 📦 打包与部署

#### 使用 Makefile

```bash
# 安装到系统
make install

# 直接运行
make run

# 生成报告
make report

# 清理构建产物
make clean
```

#### 独立脚本

DevGuardian 是单个 Python 文件，可直接运行：

```bash
chmod +x devguardian.py
./devguardian.py
```

### 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🇹