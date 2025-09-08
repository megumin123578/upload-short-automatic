# ─────────────────────────────────────────────────────────────
# Project layout (all files below can live in the same folder)
# ─────────────────────────────────────────────────────────────

# =====================
# utils.py
# =====================


# =====================
# ui_actions.py
# =====================
# Lớp bọc các thao tác UI. Em có thể map sang các hàm sẵn có trong module của em.
import time, random, pyautogui, pyperclip
from typing import Tuple

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def random_delay(a: float = 0.3, b: float = 0.6):
    time.sleep(random.uniform(a, b))


def random_mouse():
    x, y = random.uniform(200, 800), random.uniform(200, 600)
    pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.4))


def access_yt_channel(url: str):
    import webbrowser
    webbrowser.open(url, new=0, autoraise=True)


def select_channel_by_handle(handle: str) -> Tuple[int, int]:
    # Tuỳ UI của em, tạm để click vị trí chung
    time.sleep(3)
    x, y = random.uniform(860, 940), random.uniform(660, 680)
    pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.4))
    pyautogui.click()
    return int(x), int(y)


def choose_file_via_dialog(folder: str, filename: str):
    # Nhập đường dẫn trực tiếp: Win: Ctrl+L trong file dialog
    time.sleep(1)
    pyautogui.hotkey('alt', 'd')  # focus path bar
    random_delay()
    pyperclip.copy(folder)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)
    # search filename
    pyperclip.copy(filename)
    pyautogui.hotkey('ctrl', 'f')
    random_delay()
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')  # open


def paste_text(text: str):
    pyperclip.copy(text)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')


# =====================
# worker.py
# =====================
import os, sys, time, random, traceback
from datetime import datetime
from utils import log, move_to_done
from ui_actions import (
    access_yt_channel,
    select_channel_by_handle,
    random_delay,
    random_mouse,
    choose_file_via_dialog,
    paste_text,
)

# Các hook để tuỳ biến theo module cũ (nếu có)
try:
    from module import increase_hash_number, get_date, ad_suitability
except Exception:
    def increase_hash_number(s: str) -> str:
        return s
    def get_date():
        today = datetime.now().strftime('%d/%m/%Y')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        return today, tomorrow
    def ad_suitability():
        pass


def upload_one(channel_url: str, handle: str, video_path: str, schedule_date: str, schedule_time: str) -> bool:
    log(f"Start upload: {handle} | {video_path} | {schedule_date} {schedule_time}")

    # 1) Open channel + select
    access_yt_channel(channel_url)
    time.sleep(4)
    select_channel_by_handle(handle)

    # 2) Open upload dialog (tuỳ UI em chỉnh thêm—ví dụ 'Create' -> 'Upload video')
    # Ở đây để trống vì UI thay đổi theo tài khoản. Em có thể ghi macro phím nóng nếu có.
    time.sleep(2)

    # 3) Choose file
    folder, filename = os.path.dirname(video_path), os.path.basename(video_path)
    choose_file_via_dialog(folder, filename)
    time.sleep(2)

    # 4) Title + Description: ví dụ chọn field bằng Tab và dán nội dung cũ + tăng số #
    # (tuỳ UI, em có thể click toạ độ cố định)
    # focus Title
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.hotkey('ctrl','a'); pyautogui.hotkey('ctrl','c')
    time.sleep(0.2)
    import pyperclip
    title = pyperclip.paste()
    new_title = increase_hash_number(title)
    paste_text(new_title)

    # move to description
    pyautogui.press('tab')
    pyautogui.hotkey('ctrl','a'); pyautogui.hotkey('ctrl','c')
    time.sleep(0.2)
    description = pyperclip.paste()
    new_desc = increase_hash_number(description)
    paste_text(new_desc)

    # 5) Ad suitability (nếu cần)
    ad_suitability()

    # 6) Scroll xuống Schedule và set thời gian (toạ độ tuỳ UI)
    time.sleep(1)
    # Ví dụ: Alt+S mở schedule nếu có accelerator; nếu không thì pyautogui.moveTo(...) như code của em
    # --- set date ---
    pyautogui.press('tab'); pyautogui.press('tab')  # jump đến date input (tuỳ UI)
    pyautogui.hotkey('ctrl','a')
    paste_text(schedule_date)
    time.sleep(0.1)
    pyautogui.press('enter')

    # --- set time ---
    pyautogui.press('tab')
    pyautogui.hotkey('ctrl','a')
    paste_text(schedule_time)
    time.sleep(0.1)
    pyautogui.press('enter')

    # 7) Publish/Schedule (click nút)
    time.sleep(1)
    pyautogui.press('tab'); pyautogui.press('enter')

    # 8) Close dialog, optional
    time.sleep(2)
    pyautogui.hotkey('ctrl','w')

    # 9) Move file to done
    move_to_done(video_path, '1. ĐÃ UP')
    log(f"Uploaded OK: {video_path}")
    return True


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
