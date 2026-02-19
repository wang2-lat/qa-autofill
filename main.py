import typer
from rich.console import Console
from rich.table import Table
import json
from pathlib import Path
from typing import Optional
import pandas as pd
from difflib import SequenceMatcher

app = typer.Typer(help="Automate security questionnaire filling")
console = Console()

DB_FILE = Path("qa_database.json")

def load_db():
    if not DB_FILE.exists():
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

@app.command()
def add(question: str, answer: str):
    """Add a new Q&A pair to the database"""
    db = load_db()
    q_id = str(len(db) + 1)
    db[q_id] = {"question": question, "answer": answer}
    save_db(db)
    console.print(f"[green]Added Q&A pair with ID: {q_id}[/green]")

@app.command()
def list():
    """List all Q&A pairs"""
    db = load_db()
    if not db:
        console.print("[yellow]No Q&A pairs found[/yellow]")
        return
    
    table = Table(title="Q&A Database")
    table.add_column("ID", style="cyan")
    table.add_column("Question", style="magenta")
    table.add_column("Answer", style="green")
    
    for q_id, data in db.items():
        table.add_row(q_id, data["question"][:50] + "...", data["answer"][:50] + "...")
    
    console.print(table)

@app.command()
def delete(q_id: str):
    """Delete a Q&A pair by ID"""
    db = load_db()
    if q_id in db:
        del db[q_id]
        save_db(db)
        console.print(f"[green]Deleted Q&A pair {q_id}[/green]")
    else:
        console.print(f"[red]Q&A pair {q_id} not found[/red]")

@app.command()
def update(q_id: str, question: Optional[str] = None, answer: Optional[str] = None):
    """Update a Q&A pair"""
    db = load_db()
    if q_id not in db:
        console.print(f"[red]Q&A pair {q_id} not found[/red]")
        return
    
    if question:
        db[q_id]["question"] = question
    if answer:
        db[q_id]["answer"] = answer
    
    save_db(db)
    console.print(f"[green]Updated Q&A pair {q_id}[/green]")

@app.command()
def fill(
    input_file: str,
    output_file: str,
    threshold: float = typer.Option(0.6, help="Similarity threshold (0-1)")
):
    """Fill questionnaire with answers from database"""
    db = load_db()
    if not db:
        console.print("[red]No Q&A pairs in database. Add some first![/red]")
        return
    
    # Read input file
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    else:
        df = pd.read_excel(input_file)
    
    if 'Question' not in df.columns:
        console.print("[red]Input file must have a 'Question' column[/red]")
        return
    
    # Add Answer column if not exists
    if 'Answer' not in df.columns:
        df['Answer'] = ''
    
    # Match and fill
    matched = 0
    for idx, row in df.iterrows():
        question = str(row['Question'])
        best_match = None
        best_score = 0
        
        for q_id, data in db.items():
            score = similarity(question, data['question'])
            if score > best_score:
                best_score = score
                best_match = data['answer']
        
        if best_score >= threshold:
            df.at[idx, 'Answer'] = best_match
            matched += 1
    
    # Save output
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        df.to_excel(output_file, index=False)
    
    console.print(f"[green]Filled {matched}/{len(df)} questions[/green]")
    console.print(f"[green]Output saved to {output_file}[/green]")

if __name__ == "__main__":
    app()
