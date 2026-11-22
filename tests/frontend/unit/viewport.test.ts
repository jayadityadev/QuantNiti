import { readFileSync } from "node:fs";
import path from "node:path";
import { describe, it, expect } from "vitest";

describe("index.html viewport", () => {
  const htmlPath = path.resolve(__dirname, "../../../index.html");
  const html = readFileSync(htmlPath, "utf8");

  it("allows pinch-zoom (WCAG 1.4.4) while keeping safe-area support", () => {
    const viewport = html.match(/<meta\s+name="viewport"\s+content="([^"]*)"/i)?.[1];

    expect(viewport).toBeDefined();
    expect(viewport).not.toMatch(/maximum-scale/i);
    expect(viewport).not.toMatch(/user-scalable/i);
    expect(viewport).toContain("viewport-fit=cover");
    expect(viewport).toContain("width=device-width");
  });
});
