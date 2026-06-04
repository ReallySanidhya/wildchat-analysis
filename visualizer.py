from IPython.display import display, HTML

def render_conversation_ui(convo, domain, topics):
    turns = len(convo) // 2
    turns_html = ""

    for turn in convo:
        role    = turn["role"]
        content = turn["content"].strip().replace("<","&lt;").replace(">","&gt;")
        is_user = role == "user"
        icon    = "U" if is_user else "A"
        role_label  = "User" if is_user else "Assistant"
        icon_color  = "#185FA5" if is_user else "#0F6E56"
        icon_bg     = "#E6F1FB" if is_user else "#E1F5EE"

        short   = content[:400]
        is_long = len(content) > 400
        rest    = content[400:] if is_long else ""
        turn_id = f"turn_{abs(hash(content))}"

        expand_btn = f"""
            <span id="{turn_id}_rest" style="display:none">{rest}</span>
            <button onclick="
                var r=document.getElementById('{turn_id}_rest');
                var b=document.getElementById('{turn_id}_btn');
                if(r.style.display==='none'){{r.style.display='inline';b.textContent='Show less'}}
                else{{r.style.display='none';b.textContent='Show more'}}
            " id="{turn_id}_btn" style="
                background:none;border:none;color:#185FA5;
                cursor:pointer;font-size:12px;padding:4px 0 0 0;display:block;">
                Show more
            </button>
        """ if is_long else ""

        turns_html += f"""
        <div style="padding:12px 16px;border-bottom:0.5px solid #e5e5e5;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <div style="width:22px;height:22px;border-radius:50%;
                    background:{icon_bg};color:{icon_color};
                    display:flex;align-items:center;justify-content:center;
                    font-size:10px;font-weight:600;flex-shrink:0;">{icon}</div>
                <span style="font-size:11px;font-weight:600;color:#888;
                    text-transform:uppercase;letter-spacing:0.06em;">{role_label}</span>
            </div>
            <div style="font-size:13px;color:#1a1a1a;line-height:1.6;padding-left:30px;">
                {short}{expand_btn}
            </div>
        </div>"""

    chips_html = "".join([
        f'<span style="font-size:12px;padding:4px 10px;border-radius:20px;'
        f'background:#f0f0f0;border:0.5px solid #ddd;color:#555;">{t}</span>'
        for t in topics
    ])

    html = f"""
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
        max-width:700px;margin:16px 0;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
            <span style="font-size:18px;font-weight:500;color:#1a1a1a;">
                WildChat conversation
            </span>
        </div>
        <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
            <span style="font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;
                background:#E6F1FB;color:#0C447C;">{domain.replace("_"," ")}</span>
            <span style="font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;
                background:#EAF3DE;color:#27500A;">{turns} turns</span>
            <span style="font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;
                background:#EEEDFE;color:#3C3489;">English</span>
        </div>
        <div style="background:#fff;border:0.5px solid #e0e0e0;
            border-radius:12px;overflow:hidden;margin-bottom:16px;">
            {turns_html}
        </div>
        <div style="margin-top:4px;">
            <p style="font-size:13px;font-weight:500;color:#555;margin-bottom:8px;">
                Detected topics
            </p>
            <div style="display:flex;flex-wrap:wrap;gap:6px;">{chips_html}</div>
        </div>
    </div>"""

    display(HTML(html))
