# TaskAutomated Backup & Rotation Script with Google Drive Integration

## Overview
This automates backups of a GitHub project by:
- Creating timestamped `.zip` backups
- Organizing backups in structured folders (Year/Month/Day)
- Uploading backups to Google Drive using **rclone**
- Implementing retention policies (daily/weekly/monthly)
- Sending webhook notifications on successful backups
- Scheduling backups via cron

## Prerequisites
- Ubuntu EC2 instance (or Linux server)
- Python 3.x
- rclone installed & configured with Google Drive
- curl installed

## Setup Instructions
1. **Install dependencies**
```bash
sudo apt update && sudo apt install -y zip unzip tree git python3 python3-pip
curl https://rclone.org/install.sh | sudo bash
pip3 install requests
```

2. **Configure rclone with Google Drive**
```bash
rclone config
```
- Select `n` for new remote
- Name it `gdrive`
- Choose `drive` (Google Drive)
- Select `n` for auto config (EC2 headless)
- Copy URL to local machine, login, get token, paste back
- Verify:
```bash
rclone listremotes
rclone ls gdrive:
```

3. **Clone GitHub project**
```bash
git clone https://github.com/your-username/your-repo.git ~/MyProject
```

4. **Run the script**
```bash
python3 backup_script.py
```

5. **Schedule with cron**
```bash
crontab -e
0 0 * * * /usr/bin/python3 /home/ubuntu/backup_script.py >> /home/ubuntu/backup/backup.log 2>&1
```

## Retention Policy
- Daily: keep last 7
- Weekly: keep last 4
- Monthly: keep last 3 months

## Example Webhook Payload
```json
{
  "project": "MyProject",
  "date": "2025-07-18 08:49:48",
  "backup_file": "MyProject_20250718_084947.zip",
  "status": "BackupSuccessful"
}
```

## Security
- Restrict IAM permissions
- Don’t commit sensitive tokens
- Use env vars for webhook URLs

