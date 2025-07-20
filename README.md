# 🤖 Clancy Discord Bot - NBA Info

This is a Python-based Discord bot that returns detailed information about NBA players using the `nba_api`.

  <img width="330" height="415" alt="image" src="https://github.com/user-attachments/assets/0ee3b667-535f-4ea4-ac71-bfa8763349d5" />  

## Features

- `!player player name` command returns:
  - Full name, height (in meters), weight (in kg)
  - Current team and position
  - College, draft year and draft pick
  - Latest season stats (PTS, AST, REB)
  - Player's official photo
  

## How to Use

### 1. Clone the repository

```bash
git clone https://github.com/your-username/nba-discord-bot.git
cd nba-discord-bot
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Create a .env file
```bash
ACESS_TOKEN=your_token_here
```
### 4. Run the bot
```bash
python main.py
```
## Available Commands
``` !ping ``` — Responds with Pong!  
```!player LeBron James ``` — Fetches complete player data  

## Credits

- [nba_api](https://github.com/swar/nba_api) — Official Python client for NBA statistics
- [discord.py](https://github.com/Rapptz/discord.py) — Python library for building Discord bots