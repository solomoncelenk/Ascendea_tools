<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bmoney Property | Deal Crunch Calculator</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --navy: #213052;
            --teal: #5fc3db;
            --teal-dark: #417d9a;
            --white: #ffffff;
            --black: #000000;
            --gray-50: #f8fafc;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-600: #475569;
            --gray-800: #1e293b;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background: var(--gray-50);
            color: var(--gray-800);
            line-height: 1.6;
        }

        /* Header */
        .header {
            background: linear-gradient(135deg, var(--navy) 0%, #1a2542 100%);
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(33, 48, 82, 0.3);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(95, 195, 219, 0.1) 0%, transparent 70%);
            pointer-events: none;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        .brand-title {
            color: var(--white);
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.25rem;
        }

        .brand-subtitle {
            color: var(--teal);
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }

        /* Layout */
        .main-layout {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 2rem;
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }

        /* Sidebar */
        .sidebar {
            background: var(--white);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--gray-200);
            height: fit-content;
            position: sticky;
            top: 2rem;
        }

        .sidebar-title {
            color: var(--navy);
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid var(--teal);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .input-group {
            margin-bottom: 1.25rem;
        }

        .input-label {
            display: block;
            color: var(--gray-600);
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .input-field {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 2px solid var(--gray-200);
            border-radius: 10px;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.2s;
            color: var(--navy);
        }

        .input-field:focus {
            outline: none;
            border-color: var(--teal);
            box-shadow: 0 0 0 3px rgba(95, 195, 219, 0.1);
        }

        .input-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
        }

        .slider-container {
            margin-top: 0.5rem;
        }

        .slider {
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: var(--gray-200);
            outline: none;
            -webkit-appearance: none;
        }

        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--teal);
            cursor: pointer;
            border: 3px solid var(--white);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .slider-value {
            text-align: right;
            color: var(--teal-dark);
            font-weight: 600;
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }

        .calculate-btn {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, var(--teal) 0%, var(--teal-dark) 100%);
            color: var(--white);
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .calculate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -5px rgba(95, 195, 219, 0.4);
        }

        /* Main Content */
        .content {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* Section Headers */
        .section-header {
            background: linear-gradient(90deg, var(--navy) 0%, var(--teal-dark) 100%);
            color: var(--white);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .section-icon {
            width: 24px;
            height: 24px;
        }

        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .metric-card {
            background: var(--white);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--gray-200);
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--teal);
        }

        .metric-label {
            color: var(--gray-600);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            color: var(--navy);
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .metric-value.positive {
            color: var(--success);
        }

        .metric-value.negative {
            color: var(--danger);
        }

        .metric-delta {
            font-size: 0.875rem;
            font-weight: 600;
            margin-top: 0.25rem;
            color: var(--gray-600);
        }

        /* Tabs */
        .tabs {
            display: flex;
            gap: 0.5rem;
            background: var(--gray-100);
            padding: 0.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }

        .tab {
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            color: var(--gray-600);
            cursor: pointer;
            transition: all 0.2s;
            border: none;
            background: transparent;
            font-size: 0.95rem;
        }

        .tab.active {
            background: var(--white);
            color: var(--navy);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .tab:hover:not(.active) {
            color: var(--navy);
        }

        /* Tab Content */
        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Data Tables */
        .data-table {
            width: 100%;
            background: var(--white);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--gray-200);
            margin-bottom: 2rem;
        }

        .data-table table {
            width: 100%;
            border-collapse: collapse;
        }

        .data-table th {
            background: var(--navy);
            color: var(--white);
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .data-table td {
            padding: 0.875rem 1rem;
            border-bottom: 1px solid var(--gray-100);
            font-weight: 500;
            color: var(--gray-800);
        }

        .data-table tr:hover {
            background: var(--gray-50);
        }

        .data-table .numeric {
            text-align: right;
            font-family: 'Inter', monospace;
            font-weight: 600;
        }

        .data-table .positive {
            color: var(--success);
            background: rgba(16, 185, 129, 0.1);
        }

        .data-table .negative {
            color: var(--danger);
            background: rgba(239, 68, 68, 0.1);
        }

        /* Two Column Layout */
        .two-col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        /* Chart Container */
        .chart-container {
            background: var(--white);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--gray-200);
            margin-bottom: 2rem;
        }

        .chart-wrapper {
            position: relative;
            height: 400px;
        }

        /* Gauge */
        .gauge-container {
            background: var(--white);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--gray-200);
            text-align: center;
        }

        .gauge-value {
            font-size: 3rem;
            font-weight: 700;
            color: var(--navy);
            margin: 1rem 0;
        }

        .gauge-label {
            color: var(--gray-600);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 0.875rem;
        }

        /* Disclaimer */
        .disclaimer {
            background: linear-gradient(135deg, rgba(95, 195, 219, 0.1) 0%, rgba(65, 125, 154, 0.05) 100%);
            border-left: 4px solid var(--teal);
            padding: 1.5rem;
            border-radius: 0 12px 12px 0;
            margin-top: 2rem;
            font-size: 0.875rem;
            color: var(--gray-600);
            line-height: 1.8;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 3rem 2rem;
            color: var(--gray-600);
            font-size: 0.875rem;
            border-top: 1px solid var(--gray-200);
            margin-top: 3rem;
        }

        .footer-links {
            margin-top: 1rem;
        }

        .footer-links a {
            color: var(--teal-dark);
            text-decoration: none;
            margin: 0 1rem;
            font-weight: 600;
        }

        .footer-links a:hover {
            color: var(--teal);
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .main-layout {
                grid-template-columns: 1fr;
            }

            .sidebar {
                position: static;
            }

            .two-col {
                grid-template-columns: 1fr;
            }

            .metrics-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
        }

        @media (max-width: 640px) {
            .brand-title {
                font-size: 1.75rem;
            }

            .metrics-grid {
                grid-template-columns: 1fr 1fr;
            }

            .metric-value {
                font-size: 1.5rem;
            }
        }

        /* Loading */
        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        .loading.active {
            display: flex;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid var(--gray-200);
            border-top-color: var(--teal);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-text {
            margin-top: 1rem;
            color: var(--navy);
            font-weight: 600;
        }
    </style>
</head>
<body>
    <!-- Loading Overlay -->
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <div class="loading-text">Crunching the numbers...</div>
    </div>

    <!-- Header -->
    <header class="header">
        <div class="container">
            <h1 class="brand-title">Bmoney Property</h1>
            <div class="brand-subtitle">Investment Grade Property Acquisition</div>
        </div>
    </header>

    <!-- Main Layout -->
    <div class="main-layout">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-title">
                <span>🎯</span> Property Details
            </div>

            <div class="input-group">
                <label class="input-label">Property Address</label>
                <input type="text" class="input-field" id="property_address" value="12 Trustcot Ave">
            </div>

            <div class="input-group">
                <label class="input-label">Purchase Price ($)</label>
                <input type="number" class="input-field" id="purchase_price" value="586000" step="1000">
            </div>

            <div class="input-group">
                <label class="input-label">Deposit (%)</label>
                <div class="slider-container">
                    <input type="range" class="slider" id="deposit_pct" min="10" max="100" value="20">
                    <div class="slider-value"><span id="deposit_val">20</span>%</div>
                </div>
            </div>

            <div class="input-group">
                <label class="input-label">Interest Rate (%)</label>
                <div class="slider-container">
                    <input type="range" class="slider" id="interest_rate" min="2" max="10" value="5.8" step="0.25">
                    <div class="slider-value"><span id="rate_val">5.8</span>%</div>
                </div>
            </div>

            <div class="sidebar-title" style="margin-top: 2rem;">
                <span>📊</span> Rental Income
            </div>

            <div class="input-row">
                <div class="input-group">
                    <label class="input-label">Low ($/wk)</label>
                    <input type="number" class="input-field" id="rent_low" value="450">
                </div>
                <div class="input-group">
                    <label class="input-label">High ($/wk)</label>
                    <input type="number" class="input-field" id="rent_high" value="550">
                </div>
            </div>

            <div class="input-group">
                <label class="input-label">Occupancy Rate (%)</label>
                <div class="slider-container">
                    <input type="range" class="slider" id="occupancy" min="80" max="100" value="92">
                    <div class="slider-value"><span id="occupancy_val">92</span>%</div>
                </div>
            </div>

            <div class="sidebar-title" style="margin-top: 2rem;">
                <span>⚙️</span> Assumptions
            </div>

            <div class="input-group">
                <label class="input-label">Capital Growth (%/yr)</label>
                <div class="slider-container">
                    <input type="range" class="slider" id="capital_growth" min="0" max="15" value="6" step="0.5">
                    <div class="slider-value"><span id="growth_val">6</span>%</div>
                </div>
            </div>

            <div class="input-group">
                <label class="input-label">Management Fee (%)</label>
                <div class="slider-container">
                    <input type="range" class="slider" id="management_pct" min="5" max="15" value="8" step="0.5">
                    <div class="slider-value"><span id="mgmt_val">8</span>%</div>
                </div>
            </div>

            <button class="calculate-btn" onclick="calculateAll()">
                Calculate Deal
            </button>
        </aside>

        <!-- Main Content -->
        <main class="content">
            <!-- 5 Metrics -->
            <div class="section-header">
                <span class="section-icon">📊</span>
                5 Metrics That Matter
            </div>

            <div class="metrics-grid" id="metrics_grid">
                <div class="metric-card">
                    <div class="metric-label">Gross Rental Yield</div>
                    <div class="metric-value" id="metric_yield">3.99%</div>
                    <div class="metric-delta">Range: 3.75% - 4.22%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Cash on Cash Return</div>
                    <div class="metric-value negative" id="metric_coc">-1.74%</div>
                    <div class="metric-delta">Range: -3.45% to -0.03%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Return (incl. Growth)</div>
                    <div class="metric-value" id="metric_total" style="color: var(--teal-dark);">12.59%</div>
                    <div class="metric-delta">Growth: 6.0%/yr</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Net Profit Margin</div>
                    <div class="metric-value" id="metric_profit">10.86%</div>
                    <div class="metric-delta">After all expenses</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Initial Equity</div>
                    <div class="metric-value" id="metric_equity">$293,000</div>
                    <div class="metric-delta">50% of value</div>
                </div>
            </div>

            <!-- Tabs -->
            <div class="tabs">
                <button class="tab active" onclick="showTab('deal', this)">🏠 Deal Analysis</button>
                <button class="tab" onclick="showTab('whatif', this)">📈 What If Scenario</button>
                <button class="tab" onclick="showTab('deposit', this)">💵 Deposit Matrix</button>
            </div>

            <!-- Deal Analysis Tab -->
            <div id="deal-tab" class="tab-content active">
                <div class="two-col">
                    <div>
                        <div class="section-header">
                            <span class="section-icon">💰</span> Cash Flow Analysis
                        </div>
                        <div class="data-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Metric</th>
                                        <th class="numeric">Monthly</th>
                                        <th class="numeric">Annual</th>
                                    </tr>
                                </thead>
                                <tbody id="cashflow_table">
                                    <tr>
                                        <td>Rental Income (Low)</td>
                                        <td class="numeric">$1,800</td>
                                        <td class="numeric">$23,400</td>
                                    </tr>
                                    <tr>
                                        <td>Rental Income (High)</td>
                                        <td class="numeric">$2,200</td>
                                        <td class="numeric">$28,600</td>
                                    </tr>
                                    <tr>
                                        <td>Operating Expenses</td>
                                        <td class="numeric">$1,005 - $1,046</td>
                                        <td class="numeric">$12,062 - $12,555</td>
                                    </tr>
                                    <tr>
                                        <td>Mortgage Interest</td>
                                        <td class="numeric">$1,416</td>
                                        <td class="numeric">$16,994</td>
                                    </tr>
                                    <tr style="background: var(--gray-50); font-weight: 700;">
                                        <td>Cash Flow</td>
                                        <td class="numeric" id="cf_monthly">-$471 to -$38</td>
                                        <td class="numeric" id="cf_annual">-$5,656 to -$456</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="section-header">
                            <span class="section-icon">📋</span> Operating Expenses
                        </div>
                        <div class="data-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Expense</th>
                                        <th class="numeric">Monthly</th>
                                        <th class="numeric">Annual</th>
                                    </tr>
                                </thead>
                                <tbody id="expenses_table">
                                    <tr><td>Council Rates</td><td class="numeric">$220</td><td class="numeric">$2,637</td></tr>
                                    <tr><td>Body Corporate</td><td class="numeric">$117</td><td class="numeric">$1,400</td></tr>
                                    <tr><td>Water Rates</td><td class="numeric">$165</td><td class="numeric">$1,978</td></tr>
                                    <tr><td>Insurance</td><td class="numeric">$165</td><td class="numeric">$1,978</td></tr>
                                    <tr><td>Repairs & Maintenance</td><td class="numeric">$183</td><td class="numeric">$2,198</td></tr>
                                    <tr><td>Management Fees</td><td class="numeric">$144 - $176</td><td class="numeric">$1,728 - $2,112</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div>
                        <div class="section-header">
                            <span class="section-icon">🏦</span> Acquisition Costs
                        </div>
                        <div class="data-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Item</th>
                                        <th class="numeric">Amount</th>
                                    </tr>
                                </thead>
                                <tbody id="acquisition_table">
                                    <tr><td>Purchase Price</td><td class="numeric">$586,000</td></tr>
                                    <tr><td>Deposit (20%)</td><td class="numeric">$117,200</td></tr>
                                    <tr><td>Loan Amount</td><td class="numeric">$468,800</td></tr>
                                    <tr><td>Stamp Duty</td><td class="numeric">$30,230</td></tr>
                                    <tr><td>LMI</td><td class="numeric">$0</td></tr>
                                    <tr><td>Legal Fees</td><td class="numeric">$2,000</td></tr>
                                    <tr><td>Building Inspection</td><td class="numeric">$550</td></tr>
                                    <tr style="background: var(--navy); color: white; font-weight: 700;">
                                        <td>Total Cash Required</td>
                                        <td class="numeric" id="total_cash">$149,980</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="gauge-container">
                            <div class="gauge-label">Total Cash Required</div>
                            <div class="gauge-value" id="gauge_value">$149,980</div>
                            <div style="color: var(--gray-600); font-size: 0.875rem;">
                                <span id="cash_pct">25.6%</span> of purchase price
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- What If Tab -->
            <div id="whatif-tab" class="tab-content">
                <div class="section-header">
                    <span class="section-icon">📈</span> What If Scenario Analysis
                </div>

                <div class="data-table" style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Scenario</th>
                                <th class="numeric">Loan Amount</th>
                                <th class="numeric">Interest Cost</th>
                                <th class="numeric">Rental Income</th>
                                <th class="numeric">Cash Return</th>
                                <th class="numeric">Total Return</th>
                            </tr>
                        </thead>
                        <tbody id="whatif_table">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>

                <div class="chart-container">
                    <div class="chart-wrapper">
                        <canvas id="whatifChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Deposit Tab -->
            <div id="deposit-tab" class="tab-content">
                <div class="section-header">
                    <span class="section-icon">💵</span> Deposit Required Matrix
                </div>

                <div class="data-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Purchase Price</th>
                                <th class="numeric">10% Deposit</th>
                                <th class="numeric">20% Deposit</th>
                                <th class="numeric">Stamp Duty</th>
                                <th class="numeric">Total Cash (10%)</th>
                                <th class="numeric">Total Cash (20%)</th>
                                <th class="numeric">Difference</th>
                            </tr>
                        </thead>
                        <tbody id="deposit_table">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>

                <div class="chart-container">
                    <div class="chart-wrapper">
                        <canvas id="depositChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Disclaimer -->
            <div class="disclaimer">
                <strong>Disclaimer:</strong> All calculations are based on averages and are not accurate. The assumptions made in this calculator are not suited to a person's individual circumstances. It is always advisable that a person seek financial advice prior to making a financial decision. Bmoney Property Pty Ltd nor any of its directors, associates, staff, or associated companies bear any liability from any actions derived from the contents of this report. One should always seek third party investment information from relevant parties such as legal, finance, and accountancy enquiries.
            </div>
        </main>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2025 Bmoney Property | Investment Grade Property Acquisition</p>
        <div class="footer-links">
            <a href="#">Book Consultation</a>
            <a href="#">Watch Tutorial</a>
            <a href="#">Contact Us</a>
        </div>
    </footer>

<script>
  // ===== UI Helpers =====
  const $ = (id) => document.getElementById(id);

  function clamp(n, min, max){ return Math.min(max, Math.max(min, n)); }

  function formatCurrency(num) {
    const sign = num < 0 ? "-" : "";
    const abs = Math.abs(num);
    return sign + "$" + abs.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function formatPercent(num) {
    return Number(num).toFixed(2) + "%";
  }

  // ===== Slider value mirrors =====
  $("deposit_pct").addEventListener("input", (e) => $("deposit_val").textContent = e.target.value);
  $("interest_rate").addEventListener("input", (e) => $("rate_val").textContent = e.target.value);
  $("occupancy").addEventListener("input", (e) => $("occupancy_val").textContent = e.target.value);
  $("capital_growth").addEventListener("input", (e) => $("growth_val").textContent = e.target.value);
  $("management_pct").addEventListener("input", (e) => $("mgmt_val").textContent = e.target.value);

  // ===== Tabs =====
  function showTab(tabName, btnEl) {
    document.querySelectorAll(".tab-content").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    $(tabName + "-tab").classList.add("active");
    if (btnEl) btnEl.classList.add("active");
  }

  // ===== Core Financial Logic (Standalone; matches original backend intent) =====
  // VIC stamp duty approximation as provided in your original Python backend.
  function calculateStampDutyVIC(price) {
    if (price <= 25000) return price * 0.014;
    if (price <= 130000) return 350 + (price - 25000) * 0.024;
    if (price <= 960000) return 2870 + (price - 130000) * 0.06;
    return price * 0.055;
  }

  function calculateDeal(data) {
    const purchase_price = data.purchase_price;
    const deposit_pct = data.deposit_pct;
    const interest_rate = data.interest_rate;
    const rent_low = data.rent_low;
    const rent_high = data.rent_high;
    const occupancy = data.occupancy;
    const capital_growth = data.capital_growth;
    const management_pct = data.management_pct;

    const council_rates = data.council_rates;
    const body_corp = data.body_corp;
    const water_rates = data.water_rates;
    const insurance = data.insurance;
    const repairs = data.repairs;
    const legals = data.legals;
    const building_inspection = data.building_inspection;
    const ba_fee = data.ba_fee;

    const stamp_duty = calculateStampDutyVIC(purchase_price);
    const lmi = deposit_pct >= 0.20 ? 0 : (purchase_price * (1 - deposit_pct)) * 0.02;

    const loan_amount = purchase_price * (1 - deposit_pct);
    const deposit_amount = purchase_price * deposit_pct;
    const total_cash_down = deposit_amount + stamp_duty + legals + building_inspection + ba_fee + lmi;

    // Rental income (weekly -> annual -> monthly), occupancy applied
    const annual_rent_low = rent_low * 52 * occupancy;
    const annual_rent_high = rent_high * 52 * occupancy;
    const monthly_rent_low = annual_rent_low / 12;
    const monthly_rent_high = annual_rent_high / 12;

    // Expenses
    const monthly_council = council_rates / 12;
    const monthly_body_corp = body_corp / 12;
    const monthly_water = water_rates / 12;
    const monthly_insurance = insurance / 12;
    const monthly_repairs = repairs / 12;
    const monthly_management_low = monthly_rent_low * management_pct;
    const monthly_management_high = monthly_rent_high * management_pct;

    const total_monthly_expenses_low =
      monthly_council + monthly_body_corp + monthly_water + monthly_insurance + monthly_repairs + monthly_management_low;
    const total_monthly_expenses_high =
      monthly_council + monthly_body_corp + monthly_water + monthly_insurance + monthly_repairs + monthly_management_high;

    const annual_expenses_low = total_monthly_expenses_low * 12;
    const annual_expenses_high = total_monthly_expenses_high * 12;

    // Mortgage interest-only (same as backend)
    const monthly_interest = (loan_amount * interest_rate) / 12;

    // Cash flow
    const monthly_cashflow_low = monthly_rent_low - total_monthly_expenses_low - monthly_interest;
    const monthly_cashflow_high = monthly_rent_high - total_monthly_expenses_high - monthly_interest;
    const annual_cashflow_low = monthly_cashflow_low * 12;
    const annual_cashflow_high = monthly_cashflow_high * 12;

    // Returns
    const gross_yield_low = annual_rent_low / purchase_price;
    const gross_yield_high = annual_rent_high / purchase_price;
    const cash_on_cash_low = total_cash_down > 0 ? (annual_cashflow_low / total_cash_down) : 0;
    const cash_on_cash_high = total_cash_down > 0 ? (annual_cashflow_high / total_cash_down) : 0;

    // Growth
    const annual_growth = purchase_price * capital_growth;
    const total_return_low = annual_cashflow_low + annual_growth;
    const total_return_high = annual_cashflow_high + annual_growth;
    const growth_on_cash_low = total_cash_down > 0 ? (total_return_low / total_cash_down) : 0;
    const growth_on_cash_high = total_cash_down > 0 ? (total_return_high / total_cash_down) : 0;

    // Net profit margin
    const net_profit_low = annual_rent_low - annual_expenses_low - (monthly_interest * 12);
    const net_profit_high = annual_rent_high - annual_expenses_high - (monthly_interest * 12);
    const net_profit_pct_low = annual_rent_low > 0 ? (net_profit_low / annual_rent_low) : 0;
    const net_profit_pct_high = annual_rent_high > 0 ? (net_profit_high / annual_rent_high) : 0;

    // Equity
    const equity = purchase_price - loan_amount;

    return {
      metrics: {
        gross_yield_avg: ((gross_yield_low + gross_yield_high) / 2) * 100,
        gross_yield_low: gross_yield_low * 100,
        gross_yield_high: gross_yield_high * 100,
        cash_on_cash_avg: ((cash_on_cash_low + cash_on_cash_high) / 2) * 100,
        cash_on_cash_low: cash_on_cash_low * 100,
        cash_on_cash_high: cash_on_cash_high * 100,
        total_return_avg: ((growth_on_cash_low + growth_on_cash_high) / 2) * 100,
        total_return_low: growth_on_cash_low * 100,
        total_return_high: growth_on_cash_high * 100,
        net_profit_avg: ((net_profit_pct_low + net_profit_pct_high) / 2) * 100,
        equity: equity,
        equity_pct: (equity / purchase_price) * 100
      },
      cashflow: {
        monthly_rent_low, monthly_rent_high,
        annual_rent_low, annual_rent_high,
        monthly_expenses_low: total_monthly_expenses_low,
        monthly_expenses_high: total_monthly_expenses_high,
        annual_expenses_low, annual_expenses_high,
        monthly_interest,
        annual_interest: monthly_interest * 12,
        monthly_cashflow_low, monthly_cashflow_high,
        annual_cashflow_low, annual_cashflow_high
      },
      expenses: {
        council_monthly: monthly_council, council_annual: council_rates,
        bodycorp_monthly: monthly_body_corp, bodycorp_annual: body_corp,
        water_monthly: monthly_water, water_annual: water_rates,
        insurance_monthly: monthly_insurance, insurance_annual: insurance,
        repairs_monthly: monthly_repairs, repairs_annual: repairs,
        management_low_monthly: monthly_management_low,
        management_high_monthly: monthly_management_high
      },
      acquisition: {
        purchase_price,
        deposit_amount,
        loan_amount,
        stamp_duty,
        lmi,
        legals,
        inspection: building_inspection,
        ba_fee,
        total_cash: total_cash_down
      }
    };
  }

  function calculateWhatIf(data) {
    const purchase_price = data.purchase_price;
    const rent_low = data.rent_low;
    const occupancy = data.occupancy;
    const capital_growth = data.capital_growth;

    const annual_rent = rent_low * 52 * occupancy;

    // Same "holding costs" simplification as the original backend.
    const holding_costs = purchase_price * 0.015;
    const mgmt_fees = annual_rent * 0.08;
    const total_expenses = holding_costs + mgmt_fees;

    const scenarios = [];
    const interest_rates = [0.06, 0.065, 0.07, 0.075, 0.08];
    const loan_pcts = [0.80, 0.90, 1.0, 1.05];

    for (const rate of interest_rates) {
      for (const pct of loan_pcts) {
        const loan_amt = purchase_price * pct;
        const interest_cost = loan_amt * rate;
        const capital_gain = purchase_price * capital_growth;
        const cash_return = annual_rent - interest_cost - total_expenses;
        const total_return = cash_return + capital_gain;

        let name = "";
        if (pct === 1.0) name = `100% @ ${(rate * 100).toFixed(1)}%`;
        else if (pct === 1.05) name = `105% @ ${(rate * 100).toFixed(1)}%`;
        else name = `${Math.round(pct * 100)}% @ ${(rate * 100).toFixed(1)}%`;

        scenarios.push({
          name,
          loan_amount: loan_amt,
          interest_cost,
          rental_income: annual_rent,
          expenses: total_expenses,
          cash_return,
          total_return,
          rate,
          pct
        });
      }
    }
    return { scenarios };
  }

  function calculateDepositMatrix(legals, ba_fee, building_inspection) {
    const prices = [];
    for (let p = 486000; p < 687000; p += 25000) prices.push(p);

    const matrix = prices.map((price) => {
      const sd = calculateStampDutyVIC(price);
      const deposit_10 = price * 0.10;
      const deposit_20 = price * 0.20;
      const total_10 = deposit_10 + sd + legals + ba_fee + building_inspection;
      const total_20 = deposit_20 + sd + legals + ba_fee + building_inspection;

      return {
        price,
        deposit_10,
        deposit_20,
        stamp_duty: sd,
        total_10,
        total_20,
        difference: total_20 - total_10
      };
    });

    return { matrix };
  }

  // ===== Renderers =====
  let whatifChartInstance = null;
  let depositChartInstance = null;

  function updateMetrics(result) {
    $("metric_yield").textContent = formatPercent(result.metrics.gross_yield_avg);

    const cocEl = $("metric_coc");
    cocEl.textContent = formatPercent(result.metrics.cash_on_cash_avg);
    cocEl.className = "metric-value " + (result.metrics.cash_on_cash_avg >= 0 ? "positive" : "negative");

    $("metric_total").textContent = formatPercent(result.metrics.total_return_avg);
    $("metric_profit").textContent = formatPercent(result.metrics.net_profit_avg);
    $("metric_equity").textContent = formatCurrency(result.metrics.equity);
  }

  function updateCashflow(result) {
    const cf = result.cashflow;
    $("cf_monthly").textContent = `${formatCurrency(cf.monthly_cashflow_low)} to ${formatCurrency(cf.monthly_cashflow_high)}`;
    $("cf_annual").textContent  = `${formatCurrency(cf.annual_cashflow_low)} to ${formatCurrency(cf.annual_cashflow_high)}`;
  }

  function updateExpenses(result) {
    const ex = result.expenses;
    $("expenses_table").innerHTML = `
      <tr><td>Council Rates</td><td class="numeric">${formatCurrency(ex.council_monthly)}</td><td class="numeric">${formatCurrency(ex.council_annual)}</td></tr>
      <tr><td>Body Corporate</td><td class="numeric">${formatCurrency(ex.bodycorp_monthly)}</td><td class="numeric">${formatCurrency(ex.bodycorp_annual)}</td></tr>
      <tr><td>Water Rates</td><td class="numeric">${formatCurrency(ex.water_monthly)}</td><td class="numeric">${formatCurrency(ex.water_annual)}</td></tr>
      <tr><td>Insurance</td><td class="numeric">${formatCurrency(ex.insurance_monthly)}</td><td class="numeric">${formatCurrency(ex.insurance_annual)}</td></tr>
      <tr><td>Repairs & Maintenance</td><td class="numeric">${formatCurrency(ex.repairs_monthly)}</td><td class="numeric">${formatCurrency(ex.repairs_annual)}</td></tr>
      <tr><td>Management Fees</td><td class="numeric">${formatCurrency(ex.management_low_monthly)} - ${formatCurrency(ex.management_high_monthly)}</td><td class="numeric">${formatCurrency(ex.management_low_monthly * 12)} - ${formatCurrency(ex.management_high_monthly * 12)}</td></tr>
    `;
  }

  function updateAcquisition(result) {
    const acq = result.acquisition;
    $("total_cash").textContent = formatCurrency(acq.total_cash);
    $("gauge_value").textContent = formatCurrency(acq.total_cash);
    $("cash_pct").textContent = ((acq.total_cash / acq.purchase_price) * 100).toFixed(1) + "%";
  }

  function updateWhatIf(result) {
    $("whatif_table").innerHTML = result.scenarios.map((s) => `
      <tr>
        <td><strong>${s.name}</strong></td>
        <td class="numeric">${formatCurrency(s.loan_amount)}</td>
        <td class="numeric">${formatCurrency(s.interest_cost)}</td>
        <td class="numeric">${formatCurrency(s.rental_income)}</td>
        <td class="numeric ${s.cash_return >= 0 ? "positive" : "negative"}">${formatCurrency(s.cash_return)}</td>
        <td class="numeric">${formatCurrency(s.total_return)}</td>
      </tr>
    `).join("");

    // Chart
    const ctx = $("whatifChart").getContext("2d");
    if (whatifChartInstance) whatifChartInstance.destroy();

    const rates = [0.06, 0.07, 0.08];
    const labels = ["80%", "90%", "100%", "105%"];
    const datasets = rates.map((rate) => {
      const rateData = result.scenarios.filter((s) => Math.abs(s.rate - rate) < 0.001).sort((a,b)=>a.pct-b.pct);
      return {
        label: (rate * 100).toFixed(1) + "% Interest",
        data: rateData.map((s) => s.cash_return),
        tension: 0.35
      };
    });

    whatifChartInstance = new Chart(ctx, {
      type: "line",
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: { display: true, text: "Cash Return by Loan Amount & Interest Rate", font: { size: 16, weight: "bold" } }
        },
        scales: {
          y: {
            ticks: { callback: (v) => "$" + Number(v).toLocaleString() }
          }
        }
      }
    });
  }

  function updateDepositMatrix(result) {
    $("deposit_table").innerHTML = result.matrix.map((m) => `
      <tr>
        <td><strong>${formatCurrency(m.price)}</strong></td>
        <td class="numeric">${formatCurrency(m.deposit_10)}</td>
        <td class="numeric">${formatCurrency(m.deposit_20)}</td>
        <td class="numeric">${formatCurrency(m.stamp_duty)}</td>
        <td class="numeric">${formatCurrency(m.total_10)}</td>
        <td class="numeric">${formatCurrency(m.total_20)}</td>
        <td class="numeric">${formatCurrency(m.difference)}</td>
      </tr>
    `).join("");

    // Chart
    const ctx = $("depositChart").getContext("2d");
    if (depositChartInstance) depositChartInstance.destroy();

    depositChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels: result.matrix.map((m) => (m.price / 1000).toFixed(0) + "k"),
        datasets: [
          { label: "10% Deposit Scenario", data: result.matrix.map((m) => m.total_10) },
          { label: "20% Deposit Scenario", data: result.matrix.map((m) => m.total_20) }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: { display: true, text: "Total Cash Required by Purchase Price", font: { size: 16, weight: "bold" } }
        },
        scales: {
          y: { ticks: { callback: (v) => "$" + Number(v).toLocaleString() } }
        }
      }
    });
  }

  // ===== Main runner =====
  function readInputs() {
    const purchase_price = parseFloat($("purchase_price").value || "0");
    const deposit_pct = parseFloat($("deposit_pct").value || "0") / 100;
    const interest_rate = parseFloat($("interest_rate").value || "0") / 100;
    const rent_low = parseFloat($("rent_low").value || "0");
    const rent_high = parseFloat($("rent_high").value || "0");
    const occupancy = parseFloat($("occupancy").value || "0") / 100;
    const capital_growth = parseFloat($("capital_growth").value || "0") / 100;
    const management_pct = parseFloat($("management_pct").value || "0") / 100;

    return {
      purchase_price: clamp(purchase_price, 0, 100000000),
      deposit_pct: clamp(deposit_pct, 0, 1),
      interest_rate: clamp(interest_rate, 0, 1),
      rent_low: clamp(rent_low, 0, 100000),
      rent_high: clamp(rent_high, 0, 100000),
      occupancy: clamp(occupancy, 0, 1),
      capital_growth: clamp(capital_growth, 0, 1),
      management_pct: clamp(management_pct, 0, 1),

      // Fixed/default annual operating costs (from your original spec)
      council_rates: 2637,
      body_corp: 1400,
      water_rates: 1977.75,
      insurance: 1977.75,
      repairs: 2197.5,
      legals: 2000,
      building_inspection: 550,
      ba_fee: 0
    };
  }

  async function calculateAll() {
    const loading = $("loading");
    loading.classList.add("active");

    try {
      const data = readInputs();

      const deal = calculateDeal(data);
      updateMetrics(deal);
      updateCashflow(deal);
      updateExpenses(deal);
      updateAcquisition(deal);

      const whatif = calculateWhatIf(data);
      updateWhatIf(whatif);

      const deposit = calculateDepositMatrix(2000, 0, 550);
      updateDepositMatrix(deposit);

    } catch (err) {
      console.error(err);
      alert("Something went wrong while calculating. Check the console for details.");
    } finally {
      loading.classList.remove("active");
    }
  }

  // Initial calculation
  calculateAll();
</script>
</body>
</html>
