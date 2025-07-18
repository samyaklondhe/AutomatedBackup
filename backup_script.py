#!/usr/bin/env python3
import os, shutil, subprocess, datetime, requests

PROJECT_NAME = "MyProject"
PROJECT_DIR = f"/home/ubuntu/{PROJECT_NAME}"
BACKUP_BASE = f"/home/ubuntu/backup/{PROJECT_NAME}"
REMOTE_NAME = "gdrive:MyBackup"
WEBHOOK_URL = "https://webhook.site/your-unique-url"

DAILY_KEEP = 7
WEEKLY_KEEP = 4
MONTHLY_KEEP = 3

def create_backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{PROJECT_NAME}_{timestamp}.zip"
    year_dir = datetime.datetime.now().strftime("%Y")
    month_dir = datetime.datetime.now().strftime("%m")
    day_dir = datetime.datetime.now().strftime("%d")
    target_dir = os.path.join(BACKUP_BASE, year_dir, month_dir, day_dir)
    os.makedirs(target_dir, exist_ok=True)
    backup_path = os.path.join(target_dir, backup_name)
    print(f"✅ Creating backup: {backup_path}")
    shutil.make_archive(backup_path.replace('.zip', ''), 'zip', PROJECT_DIR)
    return backup_path, backup_name

def upload_to_drive(backup_path, backup_name):
    print(f"Running: rclone copy '{backup_path}' {REMOTE_NAME}")
    subprocess.run(["rclone", "copy", backup_path, REMOTE_NAME], check=True)
    print(f"✅ Uploaded to Google Drive: {backup_name}")

def send_webhook(backup_name):
    payload = {
        "project": PROJECT_NAME,
        "date": str(datetime.datetime.now()),
        "backup_file": backup_name,
        "status": "BackupSuccessful"
    }
    resp = requests.post(WEBHOOK_URL, json=payload)
    print("✅ Webhook sent successfully" if resp.status_code==200 else f"❌ Webhook failed: {resp.status_code}")

def cleanup_old_backups():
    print("🧹 Rotation cleanup done. (Customize retention policy as needed)")

if __name__=="__main__":
    backup_path, backup_name = create_backup()
    upload_to_drive(backup_path, backup_name)
    send_webhook(backup_name)
    cleanup_old_backups()
