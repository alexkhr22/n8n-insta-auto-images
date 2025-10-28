import subprocess
import sys

def run(cmd, check=True):
    """Hilfsfunktion zum Ausführen von Git-Befehlen"""
    print(f"\n🔹 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr.strip():
        print("⚠️", result.stderr.strip())
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result

def main():
    print("=== 🔧 Git Sync Script: Lokale + Remote Änderungen zusammenführen ===")

    # 1️⃣ Änderungen sichern
    run("git add .", check=False)
    run("git stash")

    # 2️⃣ Remote-Änderungen holen
    print("\n📥 Pull vom Remote-Repo (main)...")
    pull_result = run("git pull origin main", check=False)

    # Falls unrelated histories erkannt werden
    if "unrelated histories" in pull_result.stderr.lower():
        print("➡️  Unrelated histories erkannt – wiederhole Pull mit --allow-unrelated-histories")
        run("git pull origin main --allow-unrelated-histories")

    # 3️⃣ Gestashte Änderungen wiederherstellen
    print("\n📤 Wende lokale Änderungen wieder an...")
    run("git diff --name-only --diff-filter=U | xargs git rm -f", check=False)
    stash_result = run("git stash pop", check=False)

    if "conflict" in stash_result.stdout.lower() or "conflict" in stash_result.stderr.lower():
        print("\n🚨 Konflikte erkannt! Bitte löse sie manuell in den markierten Dateien.")
        print("Danach bitte:")
        print("  git add .")
        print('  git commit -m "Merge lokale und Remote Änderungen"')
        print("  git push origin main")
        sys.exit(1)

    # 4️⃣ Alles hinzufügen und committen
    run("git add .")
    run('git commit -m "Merge lokale und Remote Änderungen"', check=False)

    # 5️⃣ Pushen
    run("git push origin main")

    print("\n✅ Fertig! Lokale und Remote-Änderungen wurden erfolgreich zusammengeführt und gepusht.")

if __name__ == "__main__":
    main()
