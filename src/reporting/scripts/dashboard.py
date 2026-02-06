import pandas as pd
import os
import sys
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from advanced.ambiguity import detect_ambiguity, get_ambiguity_icons

def get_ambiguity_class(score):
    """Return CSS class based on ambiguity score."""
    if score >= 0.7:
        return "high-ambiguity"
    elif score >= 0.4:
        return "medium-ambiguity"
    elif score >= 0.1:
        return "low-ambiguity"
    else:
        return "no-ambiguity"
# Leer clusters
clusters_df = pd.read_csv(r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\data\raw\doors_exports\clusters.csv")
cluster_map = {}
for _, row in clusters_df.iterrows():
    cluster_map[row["requirement_id"]] = row["cluster_id"]

# Leer matches
MATCHES_CSV = r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\data\processed\matches.csv"
df = pd.read_csv(MATCHES_CSV)

# Agregar clusters al df para ordenar
df['Cluster1'] = df['ID1'].map(cluster_map).fillna('N/A')
df['Cluster2'] = df['ID2'].map(cluster_map).fillna('N/A')

# Ordenar por Cluster1, luego Cluster2, luego Score DESC
df = df.sort_values(by=['Cluster1', 'Cluster2', 'Score'], ascending=[True, True, False])

# Leer reqs para asignar dominios
reqs_df = pd.read_csv(r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\data\raw\doors_exports\reqs.csv")
domain_map = dict(zip(reqs_df["id"], reqs_df["domain"]))

# Calcular ambigüedad para cada requisito
ambiguity_map = {}
for _, row in reqs_df.iterrows():
    req_id = row["id"]
    req_text = row["text"]
    ambiguity_result = detect_ambiguity(req_text)
    ambiguity_map[req_id] = ambiguity_result

# Calcular conflicted_clusters
cluster_domains = {}
for _, row in clusters_df.iterrows():
    cid = row["cluster_id"]
    rid = row["requirement_id"]
    domain = domain_map.get(rid)
    cluster_domains.setdefault(cid, set()).add(domain)

conflicted_clusters = {
    cid for cid, domains in cluster_domains.items()
    if "SECURITY" in domains and "USABILITY" in domains
}

OUTPUT_HTML = r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\reports\dashboard.html"
os.makedirs(r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\reports", exist_ok=True)

# Obtener fecha y hora actual
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

summary = df['Match_Type'].value_counts().to_dict()

# Preparar clusters para HTML
clusters_html = ""
for cid in sorted(cluster_domains.keys()):
    domains = cluster_domains[cid]
    conflict_icon = "⚔️" if cid in conflicted_clusters else ""
    clusters_html += f"<h3>Cluster {cid} {conflict_icon}</h3><ul>"
    for rid in clusters_df[clusters_df["cluster_id"] == cid]["requirement_id"]:
        clusters_html += f"<li>{rid}</li>"
    clusters_html += "</ul>"

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>QA Requirement Analyzer</title>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}

        .DUPLICATE {{ background-color: #ffcccc !important; }}
        .SIMILAR {{ background-color: #fff2cc !important; }}
        .DIFFERENT {{ background-color: #ccffcc !important; }}
        
        .high-ambiguity {{ background-color: #ff6b6b !important; color: white; }}
        .medium-ambiguity {{ background-color: #ffd93d !important; }}
        .low-ambiguity {{ background-color: #6bcf7f !important; }}
        .no-ambiguity {{ background-color: #4ecdc4 !important; }}
    </style>
</head>
<body>

<h1>QA Requirement Similarity Dashboard</h1>
<p><strong>Generated on:</strong> {current_datetime}</p>

<h2>Summary</h2>
<ul>
    <li>DUPLICATE: {summary.get("DUPLICATE", 0)}</li>
    <li>SIMILAR: {summary.get("SIMILAR", 0)}</li>
    <li>DIFFERENT: {summary.get("DIFFERENT", 0)}</li>
</ul>

<h2>Clusters</h2>
{clusters_html}

<h2>Legend</h2>
<p><strong>Ambiguity Icons:</strong></p>
<ul>
    <li><strong>🔎</strong> = Needs formal review (moderate ambiguity, score ≥ 3)</li>
    <li><strong>🟠</strong> = Needs rewrite or editing (high ambiguity, score ≥ 4)</li>
</ul>

<h2>Details</h2>
<table>
<tr>
    <th>ID 1</th>
    <th>ID 2</th>
    <th>Score</th>
    <th>Match Type</th>
    <th>Cluster ID1</th>
    <th>Cluster ID2</th>
    <th>Conflict</th>
    <th>Ambiguity Score 2</th>
    <th>Ambiguity Reasons 2</th>
</tr>
"""

shown_clusters = set()

for _, row in df.iterrows():
    cluster1 = row['Cluster1']
    cluster2 = row['Cluster2']
    conflict_icon = "⚔️" if cluster1 in conflicted_clusters or cluster2 in conflicted_clusters else ""
    title_attr = ' title="SECURITY vs USABILITY"' if conflict_icon else ""
    
    display_cluster1 = cluster1 if cluster1 not in shown_clusters else ''
    display_cluster2 = cluster2 if cluster2 not in shown_clusters else ''
    
    if display_cluster1:
        shown_clusters.add(cluster1)
    if display_cluster2:
        shown_clusters.add(cluster2)
    
    # Obtener datos de ambigüedad
    amb1 = ambiguity_map.get(row['ID1'], {'ambiguity_score': 0, 'ambiguity_reasons': ''})
    amb2 = ambiguity_map.get(row['ID2'], {'ambiguity_score': 0, 'ambiguity_reasons': ''})
    
    # Determinar clases de ambigüedad
    amb_class2 = get_ambiguity_class(amb2['ambiguity_score'])
    
    # Determinar iconos de ambigüedad
    amb_icons2 = get_ambiguity_icons(amb2['ambiguity_score'])
    
    html += """
<tr class="{match_type}">
    <td>{id1}</td>
    <td>{id2}</td>
    <td>{score}</td>
    <td>{match_type}</td>
    <td>{display_cluster1}</td>
    <td>{display_cluster2}</td>
    <td{title_attr}>{conflict_icon}</td>
    <td class="{amb_class2}">{amb_score2}{amb_icons2}</td>
    <td class="{amb_class2}">{amb_reasons2}{amb_icons2}</td>
</tr>
""".format(
    match_type=row['Match_Type'],
    id1=row['ID1'],
    id2=row['ID2'],
    score=row['Score'],
    display_cluster1=display_cluster1,
    display_cluster2=display_cluster2,
    title_attr=title_attr,
    conflict_icon=conflict_icon,
    amb_class2=amb_class2,
    amb_score2=amb2['ambiguity_score'],
    amb_reasons2=amb2['ambiguity_reasons'],
    amb_icons2=amb_icons2
)

html += """
</table>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard generated at {OUTPUT_HTML}")
