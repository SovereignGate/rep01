import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor('#070D18')
ax.set_facecolor('#070D18')
ax.set_xlim(0, 1280)
ax.set_ylim(0, 720)

# Glows
ax.add_patch(plt.Circle((640, 420), 450, color='#0284C7', alpha=0.18, zorder=1))
ax.add_patch(plt.Circle((180, 560), 280, color='#6366F1', alpha=0.14, zorder=1))
ax.add_patch(plt.Circle((1100, 180), 280, color='#10B981', alpha=0.12, zorder=1))

# Badge
badge = patches.FancyBboxPatch((380, 610), 520, 42, boxstyle="round,pad=4,rounding_size=18",
                               linewidth=1.5, edgecolor='#0284C7', facecolor='#0F172A', zorder=2)
ax.add_patch(badge)
ax.text(640, 631, "MICROSOFT AGENTATHON 2026 -- TRACK 3: ARCHITECT", 
        color='#38BDF8', fontsize=12, fontweight='bold', ha='center', va='center', zorder=3)

# Title & Subtitle
ax.text(640, 530, "SOVEREIGNGATE", color='#FFFFFF', fontsize=52, fontweight='black', ha='center', va='center', zorder=3)
ax.text(640, 470, "Confidential Multi-Agent AI Gateway on Azure AI Foundry", 
        color='#94A3B8', fontsize=18, fontweight='semibold', ha='center', va='center', zorder=3)

cards = [
    ("AGENT 1: SENTINEL", "Deterministic PII Redaction\nEphemeral Memory Vault", "#0284C7"),
    ("AGENT 2: DISPATCHER", "UK DPA & GDPR Residency\nAzure UK South Node", "#8B5CF6"),
    ("AGENT 3: RECONSTRUCTOR", "Zero Retention Wipe\nTamper-Evident Audit", "#10B981")
]

for i, (title, desc, accent) in enumerate(cards):
    px = 100 + i * 380
    py = 230
    box = patches.FancyBboxPatch((px, py), 320, 140, boxstyle="round,pad=8,rounding_size=16",
                                 linewidth=1.8, edgecolor=accent, facecolor='#0F172A', zorder=2)
    ax.add_patch(box)
    strip = patches.Rectangle((px + 20, py + 134), 280, 4, facecolor=accent, zorder=3)
    ax.add_patch(strip)
    ax.text(px + 160, py + 105, title, color='#F8FAFC', fontsize=12.5, fontweight='bold', ha='center', va='center', zorder=4)
    ax.plot([px + 30, px + 290], [py + 80, py + 80], color='#334155', lw=1.2, zorder=4)
    ax.text(px + 160, py + 42, desc, color='#94A3B8', fontsize=11, ha='center', va='center', multialignment='center', zorder=4)

# Bottom metric bar
status_box = patches.FancyBboxPatch((160, 70), 960, 55, boxstyle="round,pad=4,rounding_size=12",
                                    linewidth=1.2, edgecolor='#334155', facecolor='#0F172A', zorder=2)
ax.add_patch(status_box)
ax.text(640, 97, "0.0% Leakage  *  UK DPA & GDPR Strict  *  Azure AI Foundry Native  *  Zero Data Retention", 
        color='#38BDF8', fontsize=13, fontweight='bold', ha='center', va='center', zorder=4)

ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig('/workspaces/rep01/thumbnail.png', dpi=100, facecolor=fig.get_facecolor())
print("[+] thumbnail.png generated successfully!")
