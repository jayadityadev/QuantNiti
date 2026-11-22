with open("src/app/api/app.py", "r", encoding="utf-8") as f:
    content = f.read()

target = "        return app.state.explore_service.list_explore_stocks(sector=sector, search=search, asset_class=asset_class)\n\n    return app"
if target not in content:
    target = target.replace("\n", "\r\n")

replacement = '''        return app.state.explore_service.list_explore_stocks(sector=sector, search=search, asset_class=asset_class)

    if static_dir.exists() and vite_index.exists():
        @app.get("/{full_path:path}", response_class=FileResponse, include_in_schema=False)
        async def serve_spa_fallback(full_path: str):
            potential_file = static_dir / full_path
            if potential_file.is_file():
                return FileResponse(potential_file)
            return FileResponse(vite_index)

    return app'''.replace("\n", "\r\n" if "\r\n" in content else "\n")

assert target in content, "Target not found in src/app/api/app.py"
new_content = content.replace(target, replacement, 1)

with open("src/app/api/app.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully added SPA fallback route to src/app/api/app.py")
