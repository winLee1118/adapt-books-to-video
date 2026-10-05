#!/usr/bin/env python3
"""Generate offline per-video workflow pages only with an explicit --generate request."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote

GROUPS = {
    'script_breakdown': '剧本分条', 'script_detail': '剧本细化',
    'director': '导演台本与调度', 'assets': '角色、场景与道具资产',
    'storyboards': '分镜与锚点', 'prompts': '资产与视频提示词',
    'sound': '声音、配乐与剪辑', 'qa': '验收与修复', 'other': '其他制作文件',
}
TEXT = {'.md', '.txt', '.csv', '.json', '.yaml', '.yml', '.srt', '.vtt', '.py', '.ps1'}
IMAGES = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif'}
VIDEOS = {'.mp4', '.webm', '.mov', '.m4v'}
AUDIO = {'.mp3', '.wav', '.ogg', '.m4a', '.flac'}
EXCLUDE = {'.git', '.venv', '__pycache__', 'node_modules', '.aws', '.ssh'}
CSS = '''
:root{color-scheme:light;--ink:#172a36;--muted:#637683;--line:#dce6eb;--accent:#146c68}
*{box-sizing:border-box}body{margin:0;background:#f4f7f8;color:var(--ink);font:16px/1.65 system-ui,"Microsoft YaHei",sans-serif}
header{background:#122b38;color:#fff;padding:32px max(24px,calc((100vw - 1180px)/2))}
main{max-width:1180px;margin:24px auto;padding:0 24px 48px}h1{font-size:30px;line-height:1.4;margin:8px 0}h2{margin:32px 0 12px;font-size:22px}
a{color:var(--accent);overflow-wrap:anywhere}header a{color:#a6dcd6}small,.muted{color:var(--muted)}header .muted{color:#b5c6cf}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:16px}.card,details{background:white;border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:12px}
.card h3{margin:4px 0 10px}.badge{display:inline-block;border-radius:6px;background:#e3efed;color:#125b56;padding:3px 9px;margin:3px;font-size:13px}.missing{background:#fff1de;color:#93541c}
nav{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0}input[type=search]{width:100%;padding:12px;border:1px solid var(--line);border-radius:9px;font:inherit}
summary{cursor:pointer;font-weight:650}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7f9;padding:14px;border-radius:8px;max-height:540px;overflow:auto;font:14px/1.7 ui-monospace,monospace}
img,video{max-width:100%;max-height:560px;object-fit:contain;border-radius:8px;background:#eaf0f3}audio{width:100%}.files{display:grid;gap:8px}.file-row{border-bottom:1px solid var(--line);padding:8px 0}
button{cursor:pointer;border:1px solid var(--line);border-radius:7px;padding:7px 12px;background:#fff;color:var(--ink)}.notice{border-left:4px solid #d5a255;padding:12px 16px;background:#fff9ed}.empty{color:var(--muted);padding:16px;border:1px dashed #bcccd4;border-radius:9px}
@media(max-width:600px){h1{font-size:24px}header{padding:22px}main{padding:0 16px}.card,details{padding:14px}}
'''
JS = '''
document.querySelectorAll('[data-search]').forEach(input=>input.addEventListener('input',()=>{
 const q=input.value.trim().toLowerCase();document.querySelectorAll('[data-filter]').forEach(el=>{el.hidden=!el.textContent.toLowerCase().includes(q)})}));
document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
 const text=document.getElementById(button.dataset.copy).textContent;
 try{if(!navigator.clipboard)throw Error();await navigator.clipboard.writeText(text);button.textContent='已复制'}
 catch(e){const ta=document.createElement('textarea');ta.value=text;document.body.append(ta);ta.select();const ok=document.execCommand('copy');ta.remove();button.textContent=ok?'已复制':'请选中文本复制'}
}));
'''


def esc(value):
    return html.escape(str(value), quote=True)


def project_file(root, relative):
    if isinstance(relative, str):
        relative = relative.replace('\\', '/')
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError('Expected a project-relative file path')
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError('File outside project: ' + relative)
    if any(part in EXCLUDE or part.startswith('.env') for part in Path(relative).parts):
        raise ValueError('Private configuration/cache cannot be included: ' + relative)
    return path


def identity(unit):
    for field in ('video_number', 'scene_number', 'episode_number'):
        value = unit.get(field)
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 1):
            raise ValueError(field + ' must be a positive integer')
    if unit.get('video_number') is None or not (unit.get('scene_number') or unit.get('episode_number')):
        raise ValueError('Each video requires video_number and scene_number or episode_number')
    return ' · '.join([f'第{unit[key]}{label}' for key, label in
        [('episode_number', '集'), ('scene_number', '场'), ('video_number', '条视频')] if unit.get(key)])


def page_name(unit_id):
    return 'video-' + hashlib.sha256(unit_id.encode('utf-8')).hexdigest()[:20] + '.html'


def href(path, output):
    return quote(os.path.relpath(path, output).replace(os.sep, '/'), safe='/')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def normalize_file(item):
    item = {'path': item} if isinstance(item, str) else dict(item)
    if isinstance(item.get('path'), str):
        item['path'] = item['path'].replace('\\', '/')
    if item.get('group', 'other') not in GROUPS:
        raise ValueError('Unknown file group: ' + str(item.get('group')))
    start, end = item.get('line_start'), item.get('line_end')
    if start is not None or end is not None:
        if not all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in (start, end)) or end < start:
            raise ValueError('line_start/line_end must define a positive inclusive range')
    return item


def render_file(item, root, output, key):
    path = project_file(root, item.get('path'))
    title = item.get('label') or item['path']
    status = item.get('status', '未登记状态')
    if not path.is_file():
        return f'<div class="card"><h3>{esc(title)}</h3><span class="badge missing">文件缺失／待生成</span><p>{esc(item["path"])}</p></div>'
    link = href(path, output)
    result = f'<details open><summary>{esc(title)}</summary><p><span class="badge">{esc(status)}</span> <a href="{link}">打开源文件</a> <small>{esc(item["path"])}</small></p>'
    suffix = path.suffix.lower()
    if suffix in TEXT:
        # Keep source text inert; HTML/scripts contained in documents are never executed.
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        if item.get('line_start'):
            lines = text.splitlines()
            if item['line_end'] > len(lines):
                raise ValueError('Excerpt range exceeds file: ' + item['path'])
            text = '\n'.join(lines[item['line_start'] - 1:item['line_end']])
            result += f'<p class="muted">本条内容：源文件第 {item["line_start"]}–{item["line_end"]} 行</p>'
        elif item.get('group') in {'script_breakdown', 'script_detail', 'director'}:
            result += '<p class="muted">显示完整源文件；本条归属由映射登记，不代表整份文档均属于本条。</p>'
        truncated = len(text) > 240000
        if truncated:
            text = text[:240000]
            result += '<p class="notice">文档较长，预览前 240000 个字符；完整内容请打开源文件。复制按钮复制当前预览。</p>'
        result += f'<button data-copy="{key}">复制文本</button><pre id="{key}">{esc(text)}</pre>'
    elif suffix in IMAGES:
        result += f'<img src="{link}" alt="{esc(title)}" loading="lazy">'
    elif suffix in VIDEOS:
        result += f'<video src="{link}" controls preload="metadata"></video>'
    elif suffix in AUDIO:
        result += f'<audio src="{link}" controls preload="metadata"></audio>'
    elif suffix == '.pdf':
        result += '<p class="muted">PDF 可通过源文件链接在浏览器中查看。</p>'
    else:
        result += '<p class="muted">此格式通过源文件链接打开。</p>'
    return result + '</details>'


def shell(title, header, content):
    return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style></head><body><header>{header}</header><main>{content}</main><script>{JS}</script></body></html>'


def generate(project, mapping='dashboard-map.json', output='reports/boards', refresh=False):
    root = Path(project).resolve()
    data = read_json(project_file(root, mapping))
    if data.get('schema_version') != 1:
        raise ValueError('dashboard-map schema_version must be 1')
    units = data.get('videos')
    if not isinstance(units, list) or not units:
        raise ValueError('Explicit video-unit mapping is required; do not infer numbering from filenames')
    dest = project_file(root, output)
    if dest == root or dest.is_file():
        raise ValueError('Output must be a dedicated directory inside the project')
    if dest.exists() and any(dest.iterdir()):
        if not refresh or not (dest / 'dashboard-generated.json').is_file():
            raise ValueError('Output exists; --refresh is allowed only for a previously generated dashboard')
    seen, positions = set(), set()
    for unit in units:
        uid = unit.get('id')
        if not isinstance(uid, str) or not uid or uid in seen:
            raise ValueError('Missing or duplicate video unit id')
        seen.add(uid)
        identity(unit)
        position = (unit.get('episode_number'), unit.get('scene_number'), unit['video_number'])
        if position in positions:
            raise ValueError('Duplicate scene/episode/video position')
        positions.add(position)
    release_path = root / 'active-release.json'
    release = read_json(release_path) if release_path.is_file() else {}
    jobs = {j['id']: j for j in release.get('jobs', [])}
    assets = {a['id']: a for a in release.get('assets', [])}
    shared = [normalize_file(i) for i in data.get('shared_files', [])]
    for item in shared:
        project_file(root, item.get('path'))
    inventory = []
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.resolve().is_relative_to(dest):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            checked = project_file(root, relative)
        except ValueError:
            continue
        inventory.append((relative, checked))
    all_owned, attachments = {}, {}
    for unit in units:
        items = [normalize_file(i) for i in unit.get('files', [])]
        asset_ids = list(unit.get('asset_ids', []))
        for jid in unit.get('job_ids', []):
            if jid not in jobs:
                raise ValueError('Unknown job id: ' + str(jid))
            job = jobs[jid]
            for field, group in [('prompt_path', 'prompts'), ('capability_record', 'other'), ('review_path', 'qa')]:
                if job.get(field):
                    items.append({'path': job[field], 'group': group, 'label': jid + ' · ' + field, 'status': job.get('status', '未登记')})
            asset_ids += job.get('input_ids', [])
            if job.get('result_asset_id'):
                asset_ids.append(job['result_asset_id'])
        for aid in dict.fromkeys(asset_ids):
            if aid not in assets:
                raise ValueError('Unknown asset id: ' + str(aid))
            asset = assets[aid]
            if asset.get('path'):
                items.append({'path': asset['path'], 'group': 'assets', 'label': aid, 'status': ' / '.join(str(asset.get(k, '未登记')) for k in ('evidence_status', 'generation_status', 'qa_status', 'use_status'))})
            if asset.get('prompt_path'):
                items.append({'path': asset['prompt_path'], 'group': 'prompts', 'label': aid + ' · 提示词'})
        # Preserve distinct excerpts from a shared source document.
        dedup = {}
        for raw in items:
            item = normalize_file(raw)
            project_file(root, item.get('path'))
            key = (item['path'], item.get('group', 'other'), item.get('line_start'), item.get('line_end'))
            dedup.setdefault(key, item)
            all_owned.setdefault(item['path'], set()).add(identity(unit))
        attachments[unit['id']] = list(dedup.values())
    shared_paths = {i['path'] for i in shared}
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    provenance = f'<p class="muted">生效版本 {esc(release.get("release_id", "未登记"))} · 看板快照 {esc(stamp)}（UTC）</p>'
    def file_index():
        rows = []
        for relative, path in inventory:
            owners = '、'.join(sorted(all_owned.get(relative, [])))
            label = owners or ('项目共用' if relative in shared_paths else '未归属／项目级文件')
            rows.append(f'<div class="file-row" data-filter><a href="{href(path, dest)}">{esc(relative)}</a><br><small>{esc(label)}</small></div>')
        return '<input type="search" data-search placeholder="搜索文件路径、场次、集数或视频归属" aria-label="搜索文件">' + ''.join(rows)
    pages, cards = {}, []
    nav = '<nav><a href="index.html">全部视频</a>' + ''.join(f'<a href="{page_name(u["id"])}">{esc(identity(u))}</a>' for u in units) + '</nav>'
    for unit in units:
        name = identity(unit)
        uid = unit['id']
        title = unit.get('title', '')
        content = '<p class="notice">这是制作记录的展示快照，不改变资产批准状态；缺失和未审查内容保持原状态。</p>'
        if unit.get('job_ids'):
            content += '<p>关联生成任务：' + ' '.join(f'<span class="badge">{esc(j)} · {esc(jobs[j].get("status", "未登记"))}</span>' for j in unit['job_ids']) + '</p>'
        for group, heading in GROUPS.items():
            selected = [i for i in attachments[uid] if i.get('group', 'other') == group]
            content += '<h2>' + heading + '</h2>'
            content += ''.join(render_file(i, root, dest, f'text-{group}-{n}') for n, i in enumerate(selected)) if selected else '<p class="empty">本条尚未登记此类文件；不根据文件名自动猜测。</p>'
        content += '<h2>项目共用文档</h2>' + (''.join(render_file(i, root, dest, f'shared-{n}') for n, i in enumerate(shared)) or '<p class="empty">尚未登记共用文档</p>')
        content += '<h2>工作流全部文件索引</h2><p class="muted">包含当前、历史、共用及未归属文件；以原始状态展示，不将历史文件当作生效资产。私密配置、缓存和看板输出自身不收录。</p>' + file_index()
        header = '<a href="index.html">制作看板</a><h1>' + esc(name) + '</h1><p>' + esc(title) + '</p><p>视频单元 ID：' + esc(uid) + '</p>' + provenance + nav
        pages[page_name(uid)] = shell(name, header, content)
        cards.append(f'<article class="card"><span class="badge">{esc(uid)}</span><h2>{esc(name)}</h2><p>{esc(title)}</p><a href="{page_name(uid)}">打开本条视频看板 →</a></article>')
    header = '<p>工作流制作看板 · 按视频单元</p><h1>' + esc(data.get('project_title', root.name)) + '</h1>' + provenance
    pages['index.html'] = shell('制作看板', header, '<div class="grid">' + ''.join(cards) + '</div><h2>工作流全部文件索引</h2>' + file_index())
    meta = {'schema_version': 1, 'generated_at': stamp, 'release_id': release.get('release_id'), 'mapping': mapping,
            'mapping_sha256': hashlib.sha256(project_file(root, mapping).read_bytes()).hexdigest(),
            'files': sorted(pages), 'video_count': len(units), 'indexed_file_count': len(inventory),
            'note': 'Snapshot only; obsolete pages from previous runs are retained but not linked.'}
    pages['dashboard-generated.json'] = json.dumps(meta, ensure_ascii=False, indent=2) + '\n'
    # All validation/rendering finishes before writing any output.
    for name in pages:
        target = dest / name
        if target.exists() and (target.is_symlink() or not target.is_file()):
            raise ValueError('Unsafe output target: ' + name)
    dest.mkdir(parents=True, exist_ok=True)
    for name, text in pages.items():
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=dest, delete=False) as handle:
            handle.write(text)
            temp = Path(handle.name)
        os.replace(temp, dest / name)
    return {'status': 'GENERATED', 'index': str(dest / 'index.html'), 'video_count': len(units), 'indexed_file_count': len(inventory)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--manifest', default='dashboard-map.json', help='Explicit per-video mapping, relative to project')
    parser.add_argument('--output', default='reports/boards', help='Dedicated output directory relative to project')
    parser.add_argument('--generate', action='store_true', help='Required explicit generation trigger')
    parser.add_argument('--refresh', action='store_true', help='Refresh previously generated pages; keep unrelated and obsolete files')
    args = parser.parse_args()
    if not args.generate:
        parser.error('No default generation. Pass --generate only after the user asks for a dashboard.')
    try:
        result = generate(args.project, args.manifest, args.output, args.refresh)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
