# The Missing Piece

**Every story has a piece that was lost…**

A complete fan archive for White Lily Cookie, Pure Vanilla Cookie, Golden Cheese Cookie, and The Missing Piece.

## Features

- **Full-stack web application** – React frontend + Node.js/Express backend
- **Self-hosted** – Runs on Ubuntu, Termux, proot-distro, Linux, VPS, LAN
- **API-driven** – RESTful endpoints for characters, events, theories, clues, gallery, messages, lore, timeline
- **CLI dashboard** – `./start.sh`, `./stop.sh`, `./restart.sh`
- **Backup & health** – Built-in health check and data backup
- **Responsive UI** – Mobile, tablet, desktop optimized

## Project Structure

```
the-missing-piece/
├── frontend/           # React + Vite frontend
├── backend/            # Express server
│   ├── server.js       # Entry point & route registration
│   ├── utils/
│   │   └── data.js     # JSON data persistence
│   └── routes/         # API route modules
│       ├── characters.js
│       ├── events.js
│       ├── theories.js
│       ├── clues.js
│       ├── gallery.js
│       ├── messages.js
│       ├── lore.js
│       ├── timeline.js
│       ├── admin.js
│       └── stats.js
├── data/               # JSON data files (generated)
├── public/             # Static assets for frontend
├── scripts/            # Management scripts
│   ├── start.sh
│   ├── stop.sh
│   ├── restart.sh
│   ├── backup.sh
│   └── shutdown.sh
├── .env.example        # Environment configuration
└── README.md
```

## Quick Start

### Prerequisites
- Node.js 18+ (for backend)
- npm or yarn
- Python 3.x (for some frontend tools)

### Installation

1. **Clone/setup the project:**
   ```bash
   cd the-missing-piece
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   npm install
   ```

3. **Start the server:**
   ```bash
   ./scripts/start.sh
   ```

   The server will start on `http://0.0.0.0:8080`.

4. **Build the frontend (optional):**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

5. **Access the application:**
   - Web: `http://localhost:8080`
   - API: `http://localhost:8080/api`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health status |
| GET | `/api/characters` | All characters |
| GET | `/api/events` | All events |
| GET | `/api/theories` | All theories |
| GET | `/api/clues` | All clues |
| GET | `/api/gallery` | All gallery items |
| GET | `/api/messages` | All messages |
| GET | `/api/lore` | All lore entries |
| GET | `/api/timeline` | Event timeline |
| POST | `/api/characters` | Add character (admin) |
| POST | `/api/events` | Add event (admin) |
| POST | `/api/theories` | Add theory (admin) |
| POST | `/api/clues` | Add clue (admin) |
| GET | `/api/stats` | System statistics |
| GET | `/api/admin/dashboard` | Admin dashboard stats |

## Commands

```bash
# Start the server
./scripts/start.sh

# Stop the server
./scripts/stop.sh

# Restart the server
./scripts/restart.sh

# Backup data
./scripts/backup.sh

# Shutdown server
./scripts/shutdown.sh
```

## Development

- **Frontend**: Built with React, Tailwind CSS, and modern hooks
- **Backend**: Express.js with rate limiting, CORS, and health checks
- **Database**: JSON files in `data/` (no external DB required)
- **Deployment**: Self-host anywhere with Node.js

## License

MIT
