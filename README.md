# triangular project structure

arbitrage_project/
├── backend/               
│   ├── data/              
│   │   ├── __init__.py              # Package initializer
│   │   ├── binance_data_stream.py   # Real-time data handling
│   │   ├── liquidity_filter.py      # Liquidity filtering logic
│   └── arbitrage/         
│       ├── __init__.py              # Package initializer
│       ├── arbitrage_detection.py   # Arbitrage pathfinding logic
│       ├── profit_calculator.py     # Profit calculation logic
│   ├── notifications/     
│       ├── __init__.py              # Package initializer
│       ├── telegram_alerts.py       # Telegram bot integration
│   └── utils/             
│       ├── __init__.py              # Package initializer
│       ├── helper_functions.py      # Utility functions
├── frontend/              
│   ├── templates/         
│   │   └── dashboard.html           # HTML for Django dashboard
│   ├── static/             
│   │   ├── css/                    # CSS files for styling
│   │   ├── js/                     # JavaScript files for interactivity
│   └── views/             
│       ├── dashboard_views.py      # Django views for rendering dashboard
├── config/                
│   ├── settings.py                 # Django settings file
│   ├── env.py                      # Environment variable loader
├── manage.py                       # Django management script
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
