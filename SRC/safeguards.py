import re

_RE_INJ = re.compile(r"(ignore .*instructions|system prompt|jailbreak|developer mode)", re.I)
_RE_CC  = re.compile(r"\b(?:\d[ -]?){13,19}\b")  # sehr grob: Kreditkartenmuster

def input_guard(msg: str) -> tuple[bool, str]:
    if not msg.strip():
        return False, "Bitte eine konkrete Frage stellen."
    if _RE_INJ.search(msg):
        return False, "Mögliche Prompt-Injection. Ich beantworte nur reguläre Fragen zu MediaMarkt."
    if _RE_CC.search(msg):
        return False, "Bitte keine sensiblen Daten (z. B. Kreditkartennummer) senden."
    return True, ""

def output_guard(text: str) -> str:
    return _RE_CC.sub("[entfernt]", text)
