from pathlib import Path

# 1. Update OnboardingHero.tsx
p_hero = Path("src/frontend/components/onboarding/OnboardingHero.tsx")
content_hero = p_hero.read_text(encoding="utf-8")

old_hero = 'className="fixed inset-0 z-50 overflow-y-auto flex flex-col justify-between bg-gradient-to-b from-slate-50 via-white to-violet-50/40 dark:from-slate-950 dark:via-[#100C24] dark:to-[#170E33] text-[var(--text-main)]"'
new_hero = 'className="fixed inset-0 z-50 overflow-y-auto flex flex-col justify-between bg-[#F8FAFC] dark:bg-[#0A0D14] bg-gradient-to-b from-slate-50 via-white to-violet-50 dark:from-slate-950 dark:via-[#100C24] dark:to-[#170E33] text-[var(--text-main)]"'

assert old_hero in content_hero, f"old_hero not found in {p_hero}"
content_hero = content_hero.replace(old_hero, new_hero)
p_hero.write_text(content_hero, encoding="utf-8")
print("Successfully patched OnboardingHero.tsx")

# 2. Update AppShell.tsx
p_shell = Path("src/frontend/components/layout/AppShell.tsx")
content_shell = p_shell.read_text(encoding="utf-8")

old_overlay = 'className="fixed inset-0 z-50 overflow-hidden"'
new_overlay = 'className="fixed inset-0 z-50 overflow-hidden bg-[#F8FAFC] dark:bg-[#0A0D14]"'
assert old_overlay in content_shell, f"old_overlay not found in {p_shell}"
content_shell = content_shell.replace(old_overlay, new_overlay)

old_main = '<main className="flex-1 overflow-y-auto content-bottom-safe relative">'
new_main = '<main className={`flex-1 overflow-y-auto content-bottom-safe relative ${!isOnboarded ? "invisible pointer-events-none" : ""}`} aria-hidden={!isOnboarded}>'
assert old_main in content_shell, f"old_main not found in {p_shell}"
content_shell = content_shell.replace(old_main, new_main)

p_shell.write_text(content_shell, encoding="utf-8")
print("Successfully patched AppShell.tsx")
