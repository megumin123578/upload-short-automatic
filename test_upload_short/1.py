# ─────────────────────────────────────────────────────────────
# Project layout (all files below can live in the same folder)
# ─────────────────────────────────────────────────────────────

# =====================
# utils.py
# =====================


# =====================
# worker.py
# =====================





if __name__ == '__main__':
    # argv: channel_url handle video_path schedule_date schedule_time
    try:
        _, channel_url, handle, video_path, schedule_date, schedule_time = sys.argv
    except ValueError:
        print("Usage: python worker.py <channel_url> <handle> <video_path> <YYYY-MM-DD> <HH:MM AM/PM>")
        sys.exit(2)
    ok = upload_one(channel_url, handle, video_path, schedule_date, schedule_time)
    sys.exit(0 if ok else 1)


# =====================
# manager.py
# =====================
import argparse, subprocess, shlex
from datetime import date
from utils import (
    log, move_to_done, create_sidecar
)

UPLOADS_CSV = 'uploads.csv'
CHANNELS_CSV = 'channels.csv'
UPLOADS_HEADER = [
    'id','channel','channel_url','video_path','file_sig','scheduled_date','scheduled_time',
    'status','attempts','last_error','video_url','created_at','updated_at'
]


def next_slots(slots: str, count: int) -> list:
    base = [s.strip() for s in (slots or '').split('|') if s.strip()]
    if not base:
        base = ['03:00 AM','09:00 AM','07:00 PM']
    out = []
    i = 0
    while len(out) < count:
        out.append(base[i % len(base)])
        i += 1
    return out


def _slots_list(slots: str) -> list:
    return [s.strip() for s in (slots or '').split('|') if s.strip()]


def _next_dates(start_date: datetime, days: int) -> list:
    return [(start_date.date() + timedelta(days=i)).isoformat() for i in range(days)]


def _slots_list(slots: str) -> list:
    return [s.strip() for s in (slots or '').split('|') if s.strip()]


def _next_dates(start_date: datetime, days: int) -> list:
    return [(start_date.date() + timedelta(days=i)).isoformat() for i in range(days)]


def enqueue_from_channels(limit_per_channel: Optional[int] = None) -> int:
    """
    Enqueue video cho TỪNG KÊNH dựa trên:
      - videos_per_day (tùy chọn). Nếu trống → suy ra từ số slots (>=1).
      - Nếu số video > số slot/ngày → tự tràn sang các ngày tiếp theo (xoay vòng slot).
      - --limit-per-channel: giới hạn số lượng enqueue thêm trong lần chạy này.
    """
    ensure_file(UPLOADS_CSV, UPLOADS_HEADER)
    rows = read_csv_dicts(UPLOADS_CSV)
    existing_keys = { (r['channel'], r.get('file_sig') or r['video_path']) for r in rows }

    channels = read_csv_dicts(CHANNELS_CSV)
    added = 0
    now = local_now()

    for ch in channels:
        handle = ch['handle']
        url = ch['channel_url']
        root = ch['root_folder']
        slots = _slots_list(ch.get('slots',''))
        slots = slots if slots else ['03:00 AM','09:00 AM','07:00 PM']

        # videos_per_day: nếu không có thì dùng số slot (ít nhất 1)
        vpd = ch.get('videos_per_day', '')
        try:
            videos_per_day = int(vpd) if str(vpd).strip() != '' else max(1, len(slots))
        except ValueError:
            videos_per_day = max(1, len(slots))

        mvpf = int(ch.get('max_videos_per_folder', '15'))

        want = videos_per_day
        if limit_per_channel is not None:
            want = min(want, int(limit_per_channel))

        vids = list_videos(root, mvpf)
        if not vids:
            log(f"No videos for {handle}")
            continue
        new_vids = [v for v in vids if (handle, (file_signature(v))) not in existing_keys]
        if not new_vids:
            continue

        take = new_vids[:want]
        if not take:
            continue

        n_days = max(1, (len(take) + len(slots) - 1) // len(slots))
        dates = _next_dates(now, n_days)

        i = 0
        for vp in take:
            d = dates[i // len(slots)]
            t = slots[i % len(slots)]
            row = {
                'id': str(uuid.uuid4()),
                'channel': handle,
                'channel_url': url,
                'video_path': vp,
                'file_sig': file_signature(vp),
                'scheduled_date': d,
                'scheduled_time': t,
                'status': 'pending',
                'attempts': '0',
                'last_error': '',
                'video_url': '',
                'created_at': local_now().isoformat(timespec='seconds'),
                'updated_at': local_now().isoformat(timespec='seconds'),
            }
            append_csv_dict(UPLOADS_CSV, row, UPLOADS_HEADER)
            added += 1
            i += 1

        log(f"Enqueued {len(take)} for {handle} | videos_per_day={videos_per_day} | days={n_days}")
    return added


def pick_pending(n: int) -> list:
    rows = read_csv_dicts(UPLOADS_CSV)
    pending = [r for r in rows if r['status'] == 'pending']
    return pending[:n]


def update_rows(updates: Dict[str, Dict[str, str]]):
    rows = read_csv_dicts(UPLOADS_CSV)
    changed = False
    now = local_now().isoformat(timespec='seconds')
    for r in rows:
        if r['id'] in updates:
            for k, v in updates[r['id']].items():
                r[k] = v
            r['updated_at'] = now
            changed = True
    if changed:
        write_csv_dicts(UPLOADS_CSV, rows, UPLOADS_HEADER)


def run_batch(batch_size: int):
    jobs = pick_pending(batch_size)
    if not jobs:
        log("No pending jobs.")
        return

    updates = {}
    for job in jobs:
        updates[job['id']] = {'status': 'uploading'}
    update_rows(updates)

    for job in jobs:
        cmd = f"python worker.py {shlex.quote(job['channel_url'])} {shlex.quote(job['channel'])} {shlex.quote(job['video_path'])} {shlex.quote(job['scheduled_date'])} {shlex.quote(job['scheduled_time'])}"
        log(f"RUN: {cmd}")
        try:
            rc = subprocess.call(cmd, shell=True)
            if rc == 0:
                update_rows({job['id']: {'status': 'uploaded', 'attempts': str(int(job['attempts'])+1), 'last_error': ''}})
            else:
                update_rows({job['id']: {'status': 'failed', 'attempts': str(int(job['attempts'])+1), 'last_error': f'rc={rc}'}})
        except Exception as e:
            update_rows({job['id']: {'status': 'failed', 'attempts': str(int(job['attempts'])+1), 'last_error': repr(e)}})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='YouTube Shorts Manager (CSV queue)')
    p.add_argument('--enqueue', action='store_true', help='Scan channels and enqueue videos')
    p.add_argument('--limit-per-channel', type=int, default=None, help='Max items to enqueue per channel this run')
    p.add_argument('--run', type=int, default=0, help='Run N pending uploads')
    args = p.parse_args()

    if args.enqueue:
        n = enqueue_from_channels(args.limit_per_channel)
        log(f"Enqueued total: {n}")
    if args.run:
        run_batch(args.run)


# =====================
# uploads.csv (auto‑created header)
# =====================
# id,channel,channel_url,video_path,scheduled_date,scheduled_time,status,attempts,last_error,created_at,updated_at
