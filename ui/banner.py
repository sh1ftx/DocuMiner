from rich.console import Console
from rich.markdown import Markdown

console = Console()

def show_banner():
    banner_md = r"""

 ____  ____  ____  _     _      _  _      _____ ____ 
/  _ \/  _ \/   _\/ \ /\/ \__/|/ \/ \  /|/  __//  __\
| | \|| / \||  /  | | ||| |\/||| || |\ |||  \  |  \/|
| |_/|| \_/||  \_ | \_/|| |  ||| || | \|||  /_ |    /
\____/\____/\____/\____/\_/  \|\_/\_/  \|\____\\_/\_\
                                                     


📚 **DocuMiner** - Seu assistente para mineração e estudo de documentos

👨‍💻 Desenvolvedor: Kayki Ivan (Sh1ft)  
🎯 Objetivo: Facilitar o aprendizado e análise de PDFs complexos  
⚙️ Tecnologia: Google Gemini API, Python, Rich, Automação Completa

🚀 Comece explorando seus documentos com inteligência artificial!
"""
    console.print(Markdown(banner_md))

