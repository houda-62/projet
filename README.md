Backend (FastAPI)
├── /organizers
├── /events
├── /participants
├── /wallets
├── /transactions
└── /auth (JWT)


my_event_app/
├── backend/                  # FastAPI
│   ├── app/
│   │   ├── main.py           # point d'entrée FastAPI
│   │   ├── config.py         # configs (DB, JWT, Stripe)
│   │   ├── models/           # SQLAlchemy / Tortoise
│   │   │   ├── organizer.py
│   │   │   ├── event.py
│   │   │   ├── participant.py
│   │   │   ├── wallet.py
│   │   │   └── transaction.py
│   │   ├── routers/          # endpoints API
│   │   │   ├── auth.py
│   │   │   ├── organizers.py
│   │   │   ├── events.py
│   │   │   ├── participants.py
│   │   │   ├── wallets.py
│   │   │   └── transactions.py
│   │   ├── services/         # logique métier
│   │   │   ├── qr_service.py
│   │   │   ├── wallet_service.py
│   │   │   └── payment_service.py
│   │   └── utils/            # helpers
│   │       └── jwt_utils.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                 # React
│   ├── public/               # assets, index.html
│   ├── src/
│   │   ├── App.js            # point d'entrée React
│   │   ├── index.js          # bootstrap React
│   │   ├── api/              # fonctions pour consommer FastAPI (axios/fetch)
│   │   │   └── api.js
│   │   ├── components/       # composants React
│   │   │   ├── EventForm.js
│   │   │   ├── ParticipantList.js
│   │   │   ├── WalletBalance.js
│   │   │   └── PosPayment.js
│   │   ├── pages/            # pages React
│   │   │   ├── Dashboard.js
│   │   │   └── POS.js
│   │   └── styles/           # CSS / Tailwind
│   │       └── main.css
│   ├── package.json
│   └── vite.config.js        # ou CRA si tu utilises create-react-app
│
├── docker-compose.yml        # pour lancer backend + frontend ensemble
└── README.md


























































backend/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── organizers.py
│   │       ├── events.py
│   │       ├── participants.py
│   │       ├── wallets.py
│   │       └── transactions.py
│   │
│   ├── models/
│   │   ├── organizer.py
│   │   ├── event.py
│   │   ├── participant.py
│   │   ├── wallet.py
│   │   └── transaction.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── organizer.py
│   │   ├── event.py
│   │   ├── participant.py
│   │   ├── wallet.py
│   │   └── transaction.py
│   │
│   ├── services/
│   │   ├── qr_service.py
│   │   ├── wallet_service.py
│   │   └── payment_service.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   │
│   └── utils/        # helpers non critiques uniquement
│
├── requirements.txt
├── Dockerfile
└── README.md

