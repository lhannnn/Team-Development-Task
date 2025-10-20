#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal terminal To-Do app.
Data file: ~/.todo.json
Commands: add, ls, done, undo, rm, clear
"""

"""
尝试使用分支

"""
#第一次尝试
import argparse, json, sys
from pathlib import Path
from datetime import datetime

DATA_PATH = Path.home() / ".todo.json"

def load():
    if DATA_PATH.exists():
        try:
            with DATA_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # 文件损坏时回退为空
            return {"next_id": 1, "items": []}
    return {"next_id": 1, "items": []}

def save(db):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def add_task(text):
    db = load()
    task = {
        "id": db["next_id"],
        "text": text.strip(),
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }
    db["items"].append(task)
    db["next_id"] += 1
    save(db)
    print(f"Added #{task['id']}: {task['text']}")

def list_tasks(show_all=False):
    db = load()
    items = db["items"]
    if not show_all:
        items = [t for t in items if not t["done"]]
    if not items:
        print("(empty)")
        return
    for t in items:
        mark = "✔" if t["done"] else " "
        print(f"[{mark}] #{t['id']:>3}  {t['text']}  (created {t['created_at']})")

def set_done(ids, value=True):
    db = load()
    idset = set(ids)
    found = 0
    for t in db["items"]:
        if t["id"] in idset:
            t["done"] = value
            found += 1
    save(db)
    action = "Done" if value else "Undone"
    if found == 0:
        print("No matching ids.")
    else:
        print(f"{action}: {', '.join(map(str, ids))}")

def remove(ids):
    db = load()
    idset = set(ids)
    before = len(db["items"])
    db["items"] = [t for t in db["items"] if t["id"] not in idset]
    save(db)
    print(f"Removed {before - len(db['items'])} item(s).")

def clear(confirm=False, done_only=False):
    db = load()
    if not confirm:
        print("Use --yes to confirm.")
        return
    if done_only:
        db["items"] = [t for t in db["items"] if not t["done"]]
    else:
        db["items"] = []
        db["next_id"] = 1
    save(db)
    print("Cleared.")

def main():
    p = argparse.ArgumentParser(description="Minimal terminal To-Do app")
    sub = p.add_subparsers(dest="cmd")

    pa = sub.add_parser("add", help="Add a task")
    pa.add_argument("text", nargs="+", help="task text")

    pls = sub.add_parser("ls", help="List tasks")
    pls.add_argument("-a", "--all", action="store_true", help="show all (incl. done)")

    pd = sub.add_parser("done", help="Mark tasks as done")
    pd.add_argument("ids", nargs="+", type=int)

    pu = sub.add_parser("undo", help="Mark tasks as not done")
    pu.add_argument("ids", nargs="+", type=int)

    pr = sub.add_parser("rm", help="Remove tasks by id")
    pr.add_argument("ids", nargs="+", type=int)

    pc = sub.add_parser("clear", help="Clear tasks")
    pc.add_argument("--done-only", action="store_true", help="only remove done tasks")
    pc.add_argument("-y", "--yes", action="store_true", help="confirm")

    if len(sys.argv) == 1:
        p.print_help()
        return

    args = p.parse_args()
    if args.cmd == "add":
        add_task(" ".join(args.text))
    elif args.cmd == "ls":
        list_tasks(show_all=args.all)
    elif args.cmd == "done":
        set_done(args.ids, True)
    elif args.cmd == "undo":
        set_done(args.ids, False)
    elif args.cmd == "rm":
        remove(args.ids)
    elif args.cmd == "clear":
        clear(confirm=args.yes, done_only=args.done_only)

if __name__ == "__main__":
    main()