#!/usr/bin/env python3
"""
DevGuardian - Intelligent Development Environment Resource Monitor & AI Diagnostic Engine
轻量级开发环境资源智能监控与AI诊断引擎

A lightweight, zero-dependency Python CLI tool for monitoring development environment
resources with AI-powered diagnostics and optimization suggestions.
"""

import os
import sys
import time
import json
import psutil
import threading
import argparse
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, List, Optional, Tuple, Any


class Colors:
    """Terminal color codes"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


class DevProcess:
    """Represents a development-related process"""
    def __init__(self, pid: int, name: str, cpu_percent: float, memory_mb: float,
                 status: str, created_time: float, cmdline: List[str]):
        self.pid = pid
        self.name = name
        self.cpu_percent = cpu_percent
        self.memory_mb = memory_mb
        self.status = status
        self.created_time = created_time
        self.cmdline = cmdline
        self.is_dev_tool = self._check_dev_tool()
        self.dev_category = self._categorize()

    def _check_dev_tool(self) -> bool:
        """Check if process is a development tool"""
        dev_keywords = [
            'python', 'node', 'npm', 'yarn', 'pnpm', 'docker', 'code', 'cursor',
            'windsurf', 'claude', 'codex', 'idea', 'pycharm', 'webstorm', 'vscode',
            'vim', 'nvim', 'git', 'cargo', 'rustc', 'go', 'java', 'javac', 'mvn',
            'gradle', 'webpack', 'vite', 'rollup', 'esbuild', 'tsc', 'eslint',
            'prettier', 'jest', 'pytest', 'mocha', 'docker-compose', 'kubectl',
            'helm', 'terraform', 'ansible', 'vagrant', 'virtualbox', 'vmware',
            'chrome', 'firefox', 'edge', 'electron', 'chromium'
        ]
        name_lower = self.name.lower()
        return any(keyword in name_lower for keyword in dev_keywords)

    def _categorize(self) -> str:
        """Categorize the development process"""
        name_lower = self.name.lower()
        cmd_str = ' '.join(self.cmdline).lower() if self.cmdline else ''

        categories = {
            'editor': ['code', 'cursor', 'windsurf', 'claude', 'idea', 'pycharm',
                      'webstorm', 'vscode', 'vim', 'nvim', 'sublime'],
            'terminal': ['terminal', 'iterm', 'alacritty', 'kitty', 'wezterm', 'hyper'],
            'browser': ['chrome', 'firefox', 'edge', 'chromium', 'electron'],
            'build': ['webpack', 'vite', 'rollup', 'esbuild', 'tsc', 'babel',
                     'parcel', 'gulp', 'grunt'],
            'test': ['jest', 'pytest', 'mocha', 'cypress', 'playwright', 'vitest'],
            'lint': ['eslint', 'prettier', 'black', 'flake8', 'mypy', 'pylint'],
            'container': ['docker', 'docker-compose', 'kubectl', 'helm', 'podman'],
            'language': ['python', 'node', 'npm', 'yarn', 'cargo', 'rustc', 'go',
                        'java', 'javac', 'ruby', 'php'],
            'version_control': ['git', 'svn', 'hg'],
            'ai_coding': ['claude', 'codex', 'copilot', 'cursor', 'windsurf']
        }

        for category, keywords in categories.items():
            if any(kw in name_lower or kw in cmd_str for kw in keywords):
                return category
        return 'other'


class ResourceMetrics:
    """Resource metrics collector"""
    def __init__(self, history_size: int = 60):
        self.history_size = history_size
        self.cpu_history: deque = deque(maxlen=history_size)
        self.memory_history: deque = deque(maxlen=history_size)
        self.disk_history: deque = deque(maxlen=history_size)
        self.network_history: deque = deque(maxlen=history_size)
        self.timestamp_history: deque = deque(maxlen=history_size)

    def update(self):
        """Update all metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            net_io = psutil.net_io_counters()

            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory.percent)
            self.disk_history.append(disk.percent)
            self.network_history.append((net_io.bytes_sent, net_io.bytes_recv))
            self.timestamp_history.append(datetime.now())
        except Exception:
            pass

    def get_averages(self) -> Dict[str, float]:
        """Get average metrics"""
        if not self.cpu_history:
            return {'cpu': 0, 'memory': 0, 'disk': 0}
        return {
            'cpu': sum(self.cpu_history) / len(self.cpu_history),
            'memory': sum(self.memory_history) / len(self.memory_history),
            'disk': sum(self.disk_history) / len(self.disk_history) if self.disk_history else 0
        }

    def get_trends(self) -> Dict[str, str]:
        """Analyze trends"""
        if len(self.cpu_history) < 10:
            return {'cpu': 'stable', 'memory': 'stable', 'disk': 'stable'}

        def get_trend(history: deque) -> str:
            recent = list(history)[-10:]
            first_half = sum(recent[:5]) / 5
            second_half = sum(recent[5:]) / 5
            diff = second_half - first_half
            if diff > 5:
                return 'rising'
            elif diff < -5:
                return 'falling'
            return 'stable'

        return {
            'cpu': get_trend(self.cpu_history),
            'memory': get_trend(self.memory_history),
            'disk': get_trend(self.disk_history)
        }


class AIDiagnostics:
    """AI-powered diagnostics engine"""
    def __init__(self):
        self.rules = self._load_diagnostic_rules()
        self.recommendations_cache: Dict[str, Any] = {}

    def _load_diagnostic_rules(self) -> List[Dict]:
        """Load diagnostic rules"""
        return [
            {
                'id': 'high_cpu',
                'condition': lambda m: m.get('cpu', 0) > 80,
                'severity': 'warning',
                'message': 'CPU usage is critically high',
                'suggestion': 'Consider closing unnecessary applications or investigating high CPU processes'
            },
            {
                'id': 'high_memory',
                'condition': lambda m: m.get('memory', 0) > 85,
                'severity': 'critical',
                'message': 'Memory usage is critically high',
                'suggestion': 'Close unused browser tabs, restart memory-heavy applications, or add more RAM'
            },
            {
                'id': 'high_disk',
                'condition': lambda m: m.get('disk', 0) > 90,
                'severity': 'critical',
                'message': 'Disk usage is critically high',
                'suggestion': 'Clean up temporary files, uninstall unused applications, or upgrade storage'
            },
            {
                'id': 'memory_leak_suspected',
                'condition': lambda m: m.get('memory_trend') == 'rising' and m.get('memory', 0) > 70,
                'severity': 'warning',
                'message': 'Possible memory leak detected',
                'suggestion': 'Monitor processes with increasing memory usage and consider restarting them'
            },
            {
                'id': 'too_many_browser_tabs',
                'condition': lambda m: m.get('browser_processes', 0) > 5 and m.get('browser_memory', 0) > 2000,
                'severity': 'info',
                'message': 'Browser is consuming significant memory',
                'suggestion': 'Close unused tabs or use tab management extensions'
            },
            {
                'id': 'dev_tools_overload',
                'condition': lambda m: m.get('dev_processes', 0) > 15,
                'severity': 'info',
                'message': 'Many development tools running simultaneously',
                'suggestion': 'Close unused IDE instances, terminals, or build processes'
            },
            {
                'id': 'low_resources_for_build',
                'condition': lambda m: (m.get('cpu', 0) > 60 or m.get('memory', 0) > 75) and m.get('build_running', False),
                'severity': 'warning',
                'message': 'Limited resources available for build tasks',
                'suggestion': 'Pause non-essential processes during builds for better performance'
            },
            {
                'id': 'thermal_throttling_risk',
                'condition': lambda m: m.get('cpu', 0) > 90 and m.get('cpu_trend') == 'rising',
                'severity': 'critical',
                'message': 'Risk of thermal throttling',
                'suggestion': 'Improve ventilation, close CPU-intensive applications, or check cooling system'
            }
        ]

    def analyze(self, metrics: Dict[str, Any], processes: List[DevProcess]) -> List[Dict]:
        """Analyze system state and generate diagnostics"""
        issues = []

        # Calculate additional metrics
        browser_procs = [p for p in processes if p.dev_category == 'browser']
        dev_procs = [p for p in processes if p.is_dev_tool]
        build_running = any(p.dev_category == 'build' for p in processes)

        analysis_context = {
            **metrics,
            'browser_processes': len(browser_procs),
            'browser_memory': sum(p.memory_mb for p in browser_procs),
            'dev_processes': len(dev_procs),
            'dev_memory': sum(p.memory_mb for p in dev_procs),
            'build_running': build_running
        }

        for rule in self.rules:
            try:
                if rule['condition'](analysis_context):
                    issues.append({
                        'id': rule['id'],
                        'severity': rule['severity'],
                        'message': rule['message'],
                        'suggestion': rule['suggestion']
                    })
            except Exception:
                continue

        return sorted(issues, key=lambda x: {'critical': 0, 'warning': 1, 'info': 2}[x['severity']])

    def generate_optimization_report(self, processes: List[DevProcess], metrics: Dict) -> Dict:
        """Generate optimization recommendations"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'recommendations': [],
            'potential_savings': {}
        }

        # Analyze by category
        categories: Dict[str, List[DevProcess]] = {}
        for p in processes:
            if p.dev_category not in categories:
                categories[p.dev_category] = []
            categories[p.dev_category].append(p)

        # Memory optimization opportunities
        total_dev_memory = sum(p.memory_mb for p in processes)
        duplicate_editors = [cat for cat, procs in categories.items()
                           if cat == 'editor' and len(procs) > 1]

        if duplicate_editors:
            report['recommendations'].append({
                'type': 'memory',
                'priority': 'high',
                'description': f'Multiple editor instances running ({len(categories.get("editor", []))})',
                'action': 'Consolidate work into fewer editor windows',
                'potential_savings_mb': sum(p.memory_mb for p in categories.get('editor', [])[1:])
            })

        # Browser tab optimization
        browser_procs = categories.get('browser', [])
        if len(browser_procs) > 2:
            report['recommendations'].append({
                'type': 'memory',
                'priority': 'medium',
                'description': f'Multiple browser processes ({len(browser_procs)})',
                'action': 'Close unused browser windows or tabs',
                'potential_savings_mb': sum(p.memory_mb for p in browser_procs) * 0.3
            })

        # Build process optimization
        build_procs = categories.get('build', [])
        if build_procs:
            report['recommendations'].append({
                'type': 'cpu',
                'priority': 'low',
                'description': f'Active build processes ({len(build_procs)})',
                'action': 'Monitor build times and consider incremental builds',
                'potential_savings_mb': 0
            })

        report['summary'] = {
            'total_dev_processes': len(processes),
            'total_dev_memory_mb': round(total_dev_memory, 2),
            'categories': {cat: len(procs) for cat, procs in categories.items()}
        }

        return report


class TUI:
    """Terminal User Interface"""
    def __init__(self):
        self.colors = Colors()
        self.width = 80
        self.height = 24
        self._update_terminal_size()

    def _update_terminal_size(self):
        """Update terminal dimensions"""
        try:
            import shutil
            size = shutil.get_terminal_size()
            self.width = size.columns
            self.height = size.lines
        except Exception:
            pass

    def clear(self):
        """Clear terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_header(self, title: str):
        """Draw header"""
        print(f"{self.colors.BG_BLUE}{self.colors.WHITE}{self.colors.BOLD}")
        print(f" {title:<{self.width-2}} ")
        print(f"{self.colors.RESET}")

    def draw_bar(self, label: str, value: float, max_val: float = 100,
                 width: int = 40, color_thresholds: List[Tuple[float, str]] = None):
        """Draw a progress bar"""
        if color_thresholds is None:
            color_thresholds = [(70, self.colors.GREEN), (85, self.colors.YELLOW), (100, self.colors.RED)]

        # Determine color
        color = self.colors.GREEN
        for threshold, col in sorted(color_thresholds):
            if value >= threshold:
                color = col

        # Calculate bar
        filled = int((value / max_val) * width)
        bar = "█" * filled + "░" * (width - filled)

        print(f"{label:<12} {color}{bar}{self.colors.RESET} {value:>5.1f}%")

    def draw_process_list(self, processes: List[DevProcess], max_items: int = 10):
        """Draw process list"""
        print(f"\n{self.colors.BOLD}🔧 Top Development Processes:{self.colors.RESET}")
        print(f"{'PID':<8} {'Name':<20} {'CPU%':<8} {'Memory':<10} {'Category':<12}")
        print("-" * 70)

        sorted_procs = sorted(processes, key=lambda p: p.memory_mb, reverse=True)[:max_items]
        for p in sorted_procs:
            mem_str = f"{p.memory_mb:.1f} MB"
            print(f"{p.pid:<8} {p.name[:19]:<20} {p.cpu_percent:<8.1f} {mem_str:<10} {p.dev_category:<12}")

    def draw_diagnostics(self, issues: List[Dict]):
        """Draw diagnostics panel"""
        print(f"\n{self.colors.BOLD}🔍 AI Diagnostics:{self.colors.RESET}")

        if not issues:
            print(f"{self.colors.GREEN}✓ System is healthy{self.colors.RESET}")
            return

        for issue in issues:
            severity_colors = {
                'critical': self.colors.RED,
                'warning': self.colors.YELLOW,
                'info': self.colors.BLUE
            }
            color = severity_colors.get(issue['severity'], self.colors.WHITE)
            icon = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}[issue['severity']]

            print(f"{color}{icon} {issue['message']}{self.colors.RESET}")
            print(f"   💡 {issue['suggestion']}")

    def draw_metrics(self, metrics: ResourceMetrics):
        """Draw metrics panel"""
        print(f"\n{self.colors.BOLD}📊 System Metrics:{self.colors.RESET}")

        if not metrics.cpu_history:
            print("Collecting data...")
            return

        current_cpu = metrics.cpu_history[-1] if metrics.cpu_history else 0
        current_mem = metrics.memory_history[-1] if metrics.memory_history else 0
        current_disk = metrics.disk_history[-1] if metrics.disk_history else 0

        self.draw_bar("CPU", current_cpu)
        self.draw_bar("Memory", current_mem)
        self.draw_bar("Disk", current_disk)

        # Show trends
        trends = metrics.get_trends()
        trend_icons = {'rising': '📈', 'falling': '📉', 'stable': '➡️'}
        print(f"\nTrends: CPU {trend_icons.get(trends['cpu'], '➡️')}  "
              f"Memory {trend_icons.get(trends['memory'], '➡️')}  "
              f"Disk {trend_icons.get(trends['disk'], '➡️')}")

    def draw_footer(self, refresh_interval: int):
        """Draw footer"""
        print(f"\n{self.colors.DIM}Press Ctrl+C to exit | Refresh: {refresh_interval}s | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{self.colors.RESET}")


class DevGuardian:
    """Main application class"""
    def __init__(self, refresh_interval: int = 2, history_size: int = 60):
        self.refresh_interval = refresh_interval
        self.running = False
        self.tui = TUI()
        self.metrics = ResourceMetrics(history_size)
        self.diagnostics = AIDiagnostics()
        self.last_processes: List[DevProcess] = []

    def get_dev_processes(self) -> List[DevProcess]:
        """Get all development-related processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info',
                                         'status', 'create_time', 'cmdline']):
            try:
                pinfo = proc.info
                memory_mb = pinfo['memory_info'].rss / 1024 / 1024 if pinfo['memory_info'] else 0

                dev_proc = DevProcess(
                    pid=pinfo['pid'],
                    name=pinfo['name'] or 'unknown',
                    cpu_percent=pinfo['cpu_percent'] or 0,
                    memory_mb=memory_mb,
                    status=pinfo['status'] or 'unknown',
                    created_time=pinfo['create_time'] or 0,
                    cmdline=pinfo['cmdline'] or []
                )

                if dev_proc.is_dev_tool:
                    processes.append(dev_proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes

    def update(self):
        """Update all data"""
        self.metrics.update()
        self.last_processes = self.get_dev_processes()

    def render(self):
        """Render the UI"""
        self.tui.clear()
        self.tui._update_terminal_size()
        self.tui.draw_header("🔰 DevGuardian - Development Environment Guardian")

        # Get current metrics
        averages = self.metrics.get_averages()
        trends = self.metrics.get_trends()

        # Draw metrics
        self.tui.draw_metrics(self.metrics)

        # Draw process list
        self.tui.draw_process_list(self.last_processes)

        # Run diagnostics
        analysis_metrics = {
            **averages,
            'cpu_trend': trends['cpu'],
            'memory_trend': trends['memory']
        }
        issues = self.diagnostics.analyze(analysis_metrics, self.last_processes)
        self.tui.draw_diagnostics(issues)

        # Draw footer
        self.tui.draw_footer(self.refresh_interval)

    def run(self):
        """Main loop"""
        self.running = True
        print("Starting DevGuardian... Press Ctrl+C to exit")
        time.sleep(1)

        try:
            while self.running:
                self.update()
                self.render()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the application"""
        self.running = False
        print(f"\n{Colors.GREEN}Thanks for using DevGuardian! 👋{Colors.RESET}")

    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a comprehensive report"""
        self.update()

        averages = self.metrics.get_averages()
        report = self.diagnostics.generate_optimization_report(self.last_processes, averages)

        report_text = []
        report_text.append("=" * 60)
        report_text.append("DevGuardian - Development Environment Report")
        report_text.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_text.append("=" * 60)
        report_text.append("")

        # Summary
        report_text.append("📊 Summary:")
        summary = report['summary']
        report_text.append(f"  Total Dev Processes: {summary['total_dev_processes']}")
        report_text.append(f"  Total Dev Memory: {summary['total_dev_memory_mb']:.2f} MB")
        report_text.append("")

        # Categories
        report_text.append("📁 Process Categories:")
        for cat, count in sorted(summary['categories'].items(), key=lambda x: -x[1]):
            report_text.append(f"  {cat}: {count}")
        report_text.append("")

        # Recommendations
        if report['recommendations']:
            report_text.append("💡 Optimization Recommendations:")
            for i, rec in enumerate(report['recommendations'], 1):
                report_text.append(f"\n  {i}. [{rec['priority'].upper()}] {rec['description']}")
                report_text.append(f"     Action: {rec['action']}")
                if rec['potential_savings_mb'] > 0:
                    report_text.append(f"     Potential Savings: {rec['potential_savings_mb']:.1f} MB")
        else:
            report_text.append("✓ No optimization recommendations at this time.")

        report_text.append("")
        report_text.append("=" * 60)

        report_str = "\n".join(report_text)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_str)
            print(f"Report saved to: {output_file}")

        return report_str


def main():
    parser = argparse.ArgumentParser(
        description='DevGuardian - Intelligent Development Environment Resource Monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start interactive monitoring
  %(prog)s --report           # Generate optimization report
  %(prog)s --interval 5       # Set refresh interval to 5 seconds
  %(prog)s --report -o report.txt  # Save report to file
        """
    )

    parser.add_argument('-i', '--interval', type=int, default=2,
                       help='Refresh interval in seconds (default: 2)')
    parser.add_argument('-r', '--report', action='store_true',
                       help='Generate optimization report and exit')
    parser.add_argument('-o', '--output', type=str,
                       help='Output file for report')
    parser.add_argument('--history-size', type=int, default=60,
                       help='Metrics history size (default: 60)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    guardian = DevGuardian(
        refresh_interval=args.interval,
        history_size=args.history_size
    )

    if args.report:
        print(guardian.generate_report(args.output))
    else:
        guardian.run()


if __name__ == '__main__':
    main()
