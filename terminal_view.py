import os
import pandas as pd
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align

# Initialize Rich Console
console = Console()


def get_latest_script_content():
    """
    Scans the uploads folder to find the most recently generated script.
    """
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        return None, "No uploads folder found."

    latest_time = 0
    latest_file_path = None

    # Walk through directories to find the newest '01_script.txt'
    for root, dirs, files in os.walk(uploads_dir):
        if "01_script.txt" in files:
            full_path = os.path.join(root, "01_script.txt")
            try:
                mtime = os.path.getmtime(full_path)
                if mtime > latest_time:
                    latest_time = mtime
                    latest_file_path = full_path
            except OSError:
                continue

    if latest_file_path:
        try:
            with open(latest_file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Return the file path (shortened) and the content
                display_path = "/".join(latest_file_path.split(os.sep)[-4:])
                return display_path, content
        except Exception as e:
            return None, f"Error reading file: {str(e)}"

    return None, "No scripts found yet."


def generate_dashboard():
    """
    Constructs the dashboard layout.
    """
    # 1. HEADER
    header = Panel(
        Align.center(Text("🤖 JAINIL'S YOUTUBE AUTOMATION SYSTEM", style="bold white on blue")),
        border_style="blue",
        padding=(1, 2)
    )

    # 2. RECENT ACTIVITY TABLE
    table = Table(title="📊 Recent Generations", expand=True, border_style="green")
    table.add_column("Date", style="dim", width=12)
    table.add_column("Topic", style="bold white")
    table.add_column("Score", justify="right", style="cyan")
    table.add_column("Status", justify="center", style="green")

    if os.path.exists("dashboard.csv"):
        try:
            df = pd.read_csv("dashboard.csv")
            # Show last 5 entries
            latest = df.tail(5).iloc[::-1]  # Reverse order
            for index, row in latest.iterrows():
                table.add_row(
                    str(row.get('date', 'N/A')),
                    str(row.get('topic', 'Unknown'))[:40] + "...",
                    str(row.get('score', '-')),
                    "✅ Done"
                )
        except Exception:
            table.add_row("-", "Error reading CSV", "-", "❌")
    else:
        table.add_row("-", "No Data Yet", "-", "Waiting...")

    # 3. SCRIPT PREVIEW
    path, script_content = get_latest_script_content()

    if path:
        script_display = Markdown(script_content[:1500] + "\n\n...(truncated for view)...")
        subtitle = f"📂 Source: {path}"
    else:
        script_display = Text(script_content, style="yellow")
        subtitle = "No File"

    script_panel = Panel(
        script_display,
        title="📝 LATEST SCRIPT PREVIEW",
        subtitle=subtitle,
        border_style="magenta",
        padding=(1, 2)
    )

    # 4. STATS SUMMARY (Fake logic for now, connects to CSV later)
    stats_text = Text()
    stats_text.append("🚀 System Status: ", style="bold")
    stats_text.append("ONLINE\n", style="green")
    stats_text.append("🧠 AI Model:      ", style="bold")
    stats_text.append("Gemini 2.5 Flash\n", style="purple")
    stats_text.append("📂 Storage:       ", style="bold")
    stats_text.append("Local Disk", style="blue")

    stats_panel = Panel(stats_text, title="⚙️ System Info", border_style="white")

    # ---- LAYOUT COMPOSITION ----
    layout = Layout()
    layout.split_column(
        Layout(header, size=5),
        Layout(name="body")
    )

    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )

    layout["left"].split_column(
        Layout(stats_panel, size=8),
        Layout(table)
    )

    layout["right"].update(script_panel)

    return layout


if __name__ == "__main__":
    console.clear()
    console.print("[bold yellow]Loading Dashboard...[/bold yellow]")

    # Run in a live loop to auto-refresh every 5 seconds
    with Live(generate_dashboard(), refresh_per_second=1, screen=True) as live:
        while True:
            live.update(generate_dashboard())
            time.sleep(5)  # Updates every 5 seconds