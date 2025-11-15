async function fetchBanncoinData() {
  const statusUrl = "/docs/status.json";
  const manifestUrl = "/docs/manifest.json";
  const recentUrl = "/docs/recent.json";

  try {
    const [status, manifest, recent] = await Promise.all([
      fetch(statusUrl).then(r => r.json()),
      fetch(manifestUrl).then(r => r.json()),
      fetch(recentUrl).then(r => r.json())
    ]);

    document.getElementById("height").textContent = status.height ?? "(n/a)";
    document.getElementById("difficulty").textContent = status.difficulty_bits ?? "(n/a)";
    document.getElementById("blocks").textContent = recent.recent_blocks?.length ?? 0;
    document.getElementById("version").textContent = manifest.version ?? "(unknown)";
  } catch (err) {
    console.error("Failed to fetch Banncoin data:", err);
  }
}
window.addEventListener("load", fetchBanncoinData);
