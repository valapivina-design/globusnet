#!/usr/bin/env python3
"""Rebrand to GlobusNet.org, corporate blue theme, generate new broker reviews."""
from pathlib import Path
import re
from datetime import date

ROOT = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
DOMAIN = "https://globusnet.org"
BRAND = "GlobusNet"
BRAND_FULL = "GlobusNet.org"

# ── Broker list (deduped / normalized) ──────────────────────────────
BROKERS = [
  {"name": "Nova Stock Trade", "slug": "novastocktrade", "url": "novastocktrade.com", "type": "Stock / Investment Platform", "blurb": "Users report blocked withdrawals, aggressive deposit pressure, and unverifiable regulatory claims."},
  {"name": "Golden Profit Stock", "slug": "goldenprofitstock", "url": "goldenprofitstock.com", "type": "Stock Trading Platform", "blurb": "Complaints cite fake profit displays, withdrawal fees, and unresponsive support after deposits."},
  {"name": "Hudson Capital", "slug": "hudsoncapital", "url": "hudsoncapital.space", "type": "Investment Platform", "blurb": "Unusual .space domain and reports of account lockouts after withdrawal requests raise serious concerns."},
  {"name": "Newton Crypto", "slug": "newton-crypto", "url": "", "type": "Crypto Trading Platform", "blurb": "Complaints involve unverifiable company details, deposit pressure, and difficulty withdrawing crypto funds."},
  {"name": "Axia Investments", "slug": "axiainvestments", "url": "axiainvestments.com", "type": "Investment Platform", "blurb": "Users report high-pressure sales, blocked withdrawals, and no clear regulatory registration."},
  {"name": "Eliice", "slug": "eliice", "url": "eliice.co", "alt_urls": ["eliice.com", "m.eliice.vip"], "type": "Trading / Investment App", "blurb": "Multiple related domains reported; complaints include withdrawal blocks and mirror-site confusion."},
  {"name": "ROI C Traders", "slug": "roictraders", "url": "roictraders.com", "type": "Trading Platform", "blurb": "Users report promised returns that never materialize and support disappearing after funding accounts."},
  {"name": "Coin Voya", "slug": "coinvoya", "url": "coinvoya.com", "type": "Crypto Platform", "blurb": "Complaints focus on deposit-only flows, fake balances, and inability to cash out cryptocurrency."},
  {"name": "Anya Trades", "slug": "anya-trades", "url": "", "type": "Trading Platform", "blurb": "Users describe account-manager pressure, fabricated profits, and escalating 'verification' fees."},
  {"name": "LSCGE", "slug": "lscge", "url": "lscge.com", "type": "Investment Platform", "blurb": "Reports include unverifiable licensing claims and withdrawal requests that stall indefinitely."},
  {"name": "Crypto Keeper", "slug": "cryptokeeper", "url": "", "type": "Crypto Platform", "blurb": "Complaints mention locked wallets, unexpected fees, and support that only responds to deposit inquiries."},
  {"name": "XT.com", "slug": "xt", "url": "xt.com", "type": "Crypto Exchange", "blurb": "This page compiles publicly reported user complaints about withdrawals, support, and account restrictions. Verify claims independently."},
  {"name": "FJSOI", "slug": "fjsoi", "url": "fjsoi.com", "type": "Trading / Investment Platform", "blurb": "Users report opaque ownership, blocked withdrawals, and pressure to deposit additional funds."},
  {"name": "Traze Exchange", "slug": "traze-exchange", "url": "traze-exchange.io", "type": "Crypto Exchange", "blurb": "Complaints cite frozen accounts, delayed withdrawals, and unclear regulatory oversight."},
  {"name": "Golden King Crab", "slug": "goldenkingcrab", "url": "m.goldenkingcrab.cc", "type": "Trading Platform", "blurb": "Mobile-first .cc domain with reports of deposit pressure and inability to withdraw balances."},
  {"name": "ByBiten Saki", "slug": "bybitensaki", "url": "bybitensaki.com", "type": "Crypto Platform (Clone Alert)", "blurb": "Name similarity to major brands is a classic clone-firm red flag. Users report deposit theft patterns."},
  {"name": "ByBiten Xuhf", "slug": "bybitenxuhf", "url": "bybitenxuhf.com", "type": "Crypto Platform (Clone Alert)", "blurb": "Related clone-style domain; complaints involve impersonation tactics and blocked fund access."},
  {"name": "BTCC Prox R", "slug": "btccproxr", "url": "btccproxr.com", "type": "Crypto Platform (Clone Alert)", "blurb": "Brand-lookalike naming with reports of phishing-style onboarding and withdrawal denial."},
  {"name": "Cornelian Capital Group", "slug": "corneliancapitalgroup", "url": "corneliancapitalgroup.com", "type": "Investment Platform", "blurb": "Users report polished marketing, unverifiable credentials, and stalled withdrawal processes."},
  {"name": "Truonao", "slug": "truonao", "url": "truonao.com", "type": "Trading Platform", "blurb": "Complaints include fake dashboard profits and demands for extra fees before payouts."},
  {"name": "MT10R", "slug": "mt10r", "url": "mt10r.com", "type": "Trading Platform", "blurb": "Users describe MetaTrader-style branding used to build trust while withdrawals remain blocked."},
  {"name": "Poolabu", "slug": "poolabu", "url": "poolabu.vip", "type": "Crypto / Investment Platform", "blurb": ".vip domain with reports of deposit-only activity and disappearing account managers."},
  {"name": "AUEX Trade", "slug": "auextrade", "url": "auextrade.com", "type": "Trading Platform", "blurb": "Complaints cite unregulated operations, withdrawal blocks, and high-pressure upselling."},
  {"name": "Devler App", "slug": "devlerapp", "url": "devlerapp.com", "type": "Trading App", "blurb": "App-style platform with reports of unexpected fees and inability to withdraw deposited funds."},
  {"name": "Upstream Hub", "slug": "upstream-hub", "url": "", "type": "Investment Platform", "blurb": "Users report opaque ownership, aggressive solicitation, and blocked access to funds."},
  {"name": "NC Wallet", "slug": "ncwallet", "url": "ncwallet.net", "type": "Crypto Wallet Platform", "blurb": "Complaints involve locked balances, unexpected 'unlock' fees, and unverifiable custody claims."},
  {"name": "UPT9 AI", "slug": "upt9ai", "url": "upt9ai.top", "type": "AI Trading Platform", "blurb": ".top domain and AI marketing claims with reports of fake returns and withdrawal denial."},
  {"name": "Capital Crestline", "slug": "capitalcrestline", "url": "capitalcrestline.com", "type": "Investment Platform", "blurb": "Users report professional branding paired with blocked withdrawals and fee demands."},
  {"name": "Bridgefy", "slug": "bridgefy", "url": "bridgefy.org", "type": "Platform Review", "blurb": "This page compiles publicly reported complaints tied to this domain. Verify independently before trusting any investment pitch."},
  {"name": "Forex App", "slug": "forexapp", "url": "forexapp.me", "type": "Forex Trading App", "blurb": "Complaints include manipulated trades, withdrawal blocks, and unregulated forex solicitation."},
  {"name": "Wealthtech Global", "slug": "wealthtech-global", "url": "wealthtech-global.co", "type": "Investment Platform", "blurb": "Users report high-pressure onboarding, fake performance claims, and stalled cash-outs."},
  {"name": "Novaedge Innovations", "slug": "novaedge-innovations", "url": "novaedge-innovations.com", "type": "Investment / Tech Platform", "blurb": "Complaints cite innovation marketing used to solicit deposits that cannot later be withdrawn."},
  {"name": "Coinlink Web3", "slug": "coinlink-web3", "url": "coinlink-web3.org", "type": "Web3 / Crypto Platform", "blurb": "Web3 branding with reports of locked tokens, unexpected fees, and unverifiable contracts."},
  {"name": "Cincypto", "slug": "cincypto", "url": "cincypto.ai", "type": "Crypto / AI Platform", "blurb": "AI-themed crypto platform with complaints about missing payouts and opaque company details."},
  {"name": "Tradinero", "slug": "tradinero", "url": "tradinero.io", "type": "Trading Platform", "blurb": "Users report deposit pressure, dashboard profits that cannot be withdrawn, and silent support."},
  {"name": "Storewalldex", "slug": "storewalldex", "url": "web.storewalldex.vip", "type": "Crypto Exchange", "blurb": "VIP subdomain exchange with reports of frozen accounts and blocked crypto withdrawals."},
  {"name": "Atomany", "slug": "atomany", "url": "atomany.co", "type": "Trading Platform", "blurb": "Complaints include aggressive account managers and escalating compliance fee demands."},
  {"name": "Soft Complex Trading", "slug": "soft-complex-trading", "url": "platform.soft-complex.com", "type": "Trading Platform", "blurb": "Hosted trading path with reports of opaque operators and withdrawal obstruction."},
  {"name": "COFC WSB", "slug": "cofc-wsb", "url": "cofc-wsb.xyz", "type": "Trading / Investment Platform", "blurb": ".xyz domain with cgi-style paths; users report deposit traps and unverifiable ownership."},
  {"name": "Steadfast Investment Ltd", "slug": "steadfast-investment", "url": "", "type": "Investment Platform", "blurb": "Users report polished firm naming, deposit pressure, and withdrawal requests that stall behind verification fees."},
  {"name": "Webfor99", "slug": "webfor99", "url": "webfor99.com", "type": "Trading / Investment Platform", "blurb": "Complaints cite blocked withdrawals, aggressive upselling, and unverifiable regulatory claims on webfor99.com."},
  {"name": "U-VIP Stock Insights", "slug": "u-vip-stock-insights", "url": "", "type": "Stock Tips / Investment Platform", "blurb": "VIP stock-insights branding with reports of paid signals, pressure to deposit more, and difficulty cashing out."},
  {"name": "Exglobolex", "slug": "exglobolex", "url": "", "type": "Trading / Investment Platform", "blurb": "Users describe opaque ownership, dashboard profits that cannot be withdrawn, and unresponsive support."},
  {"name": "Bitsypay H5", "slug": "bitsypay-h5", "url": "h5.bitsypay", "type": "Crypto / Payment Platform", "blurb": "Mobile H5 payment-style domain with reports of deposit traps, locked balances, and unclear operator identity."},
  {"name": "AllenAI", "slug": "allenai", "url": "allenai.com", "type": "AI Trading Platform", "blurb": "AI-branded trading pitch with complaints about fake performance claims, withdrawal blocks, and clone-style naming risks."},
  {"name": "Landmark Markets", "slug": "landmarkmarkets", "url": "landmarkmarkets.com", "type": "Trading / Investment Platform", "blurb": "Users report deposit pressure, stalled withdrawals, and unverifiable licensing claims."},
  {"name": "Alinea Invest", "slug": "alinea-invest", "url": "alinea-invest.com", "type": "Investment Platform", "blurb": "Complaints cite polished marketing, blocked cash-outs, and unclear regulatory status."},
  {"name": "Minepays", "slug": "minepays", "url": "minepays.org", "type": "Crypto / Mining Platform", "blurb": ".org mining-style pitch with reports of locked balances and missing payouts."},
  {"name": "Investment Hub", "slug": "investment-hub", "url": "investment-hub.com", "type": "Investment Platform", "blurb": "Hub-style branding with reports of aggressive solicitation and withdrawal obstruction."},
  {"name": "Groundfloor", "slug": "groundfloor", "url": "groundfloor.com", "type": "Investment Platform", "blurb": "This page compiles publicly reported user complaints. Verify independently — Groundfloor also operates as a known real-estate investing brand."},
  {"name": "Willow Wealth", "slug": "willowwealth", "url": "willowwealth.com", "type": "Wealth / Investment Platform", "blurb": "Wealth branding with complaints about deposit pressure and funds that cannot be withdrawn."},
  {"name": "Premium Yields", "slug": "premiumyields1", "url": "premiumyields1.com", "type": "Investment Platform", "blurb": "High-yield marketing with reports of fake returns and escalating fee demands."},
  {"name": "Dreams FX", "slug": "dreamsfx", "url": "dreamsfx.net", "type": "Forex Trading Platform", "blurb": "FX platform complaints include blocked withdrawals and unresponsive account managers."},
  {"name": "Spark Wealths", "slug": "sparkwealths", "url": "sparkwealths.com", "type": "Investment Platform", "blurb": "Users report spark/wealth branding paired with withdrawal denial and fee loops."},
  {"name": "Oroku Edge", "slug": "orokuedge", "url": "orokuedge.com", "type": "Trading Platform", "blurb": "Complaints cite opaque operators, deposit-only flows, and stalled payouts."},
  {"name": "JustMarkets", "slug": "justmarkets", "url": "justmarkets.eu", "type": "Forex / CFD Broker", "blurb": "This page compiles publicly reported complaints about JustMarkets.eu. Verify regulatory claims independently."},
  {"name": "MarketsAll", "slug": "marketsall", "url": "marketsall.com", "type": "Trading Platform", "blurb": "Users report withdrawal issues, pressure to deposit more, and weak regulatory proof."},
  {"name": "MinerGPT", "slug": "minergpt", "url": "minergpt.digital", "type": "AI / Mining Platform", "blurb": "AI-mining pitch with complaints about missing payouts and unverifiable company details."},
  {"name": "Binary Mate", "slug": "binarymate", "url": "binarymate.com", "type": "Binary Options Platform", "blurb": "Binary-options style complaints: deposit pressure, blocked withdrawals, and fake profits."},
  {"name": "Trade Trib Exchange", "slug": "tradetribexchange", "url": "tradetribexchange.com", "type": "Crypto Exchange", "blurb": "Exchange branding with reports of frozen accounts and delayed crypto withdrawals."},
  {"name": "Halo Investing", "slug": "haloinvesting", "url": "haloinvesting.com", "type": "Investment Platform", "blurb": "Investing pitch with complaints about unverifiable returns and cash-out problems."},
  {"name": "Star Navigation Capital", "slug": "starnavigationcapital", "url": "starnavigationcapital.com", "type": "Investment Platform", "blurb": "Capital branding with reports of stalled withdrawals and high-pressure onboarding."},
  {"name": "Trader Delta", "slug": "traderdelta", "url": "traderdelta.com", "type": "Trading Platform", "blurb": "Users describe dashboard profits that cannot be withdrawn and silent support."},
  {"name": "Ranieri Asset", "slug": "ranieriasset", "url": "ranieriasset.com", "type": "Asset / Investment Platform", "blurb": "Complaints include deposit traps, verification fee loops, and opaque ownership."},
  {"name": "Zid Finance Global", "slug": "zidfinanceglobal", "url": "zidfinanceglobal.com", "type": "Finance / Investment Platform", "blurb": "Global finance branding with reports of blocked withdrawals and unverifiable licenses."},
  {"name": "Infinity Metrix", "slug": "infinitymetrix", "url": "infinitymetrix.com", "type": "Trading / Investment Platform", "blurb": "Metrix-style platform with complaints about fake performance and payout denial."},
  {"name": "Say Trader", "slug": "saytrader", "url": "saytrader.com", "type": "Trading Platform", "blurb": "Users report account-manager pressure and inability to cash out deposited funds."},
  {"name": "Balancer Pro", "slug": "balancerpro", "url": "balancerpro.com", "type": "Trading Platform", "blurb": "Pro trading branding with reports of withdrawal blocks and fee demands."},
  {"name": "Morris Capitals", "slug": "morris-capitals", "url": "morris-capitals.com", "type": "Investment Platform", "blurb": "Capitals branding with complaints about stalled withdrawals and unverifiable credentials."},
  {"name": "Exivara24", "slug": "exivara24", "url": "exivara24.com", "type": "Trading Platform", "blurb": "24-branded trading site with reports of deposit pressure and blocked cash-outs."},
  {"name": "Onencore", "slug": "onencore", "url": "onencore.com", "type": "Investment Platform", "blurb": "Users report polished onboarding followed by withdrawal obstruction."},
  {"name": "Trade Direct 24", "slug": "tradedirect24", "url": "tradedirect24.com", "type": "Trading Platform", "blurb": "Direct-trading pitch with complaints about fake profits and unresponsive support."},
  {"name": "BitCastle", "slug": "bitcastle", "url": "bitcastle.io", "type": "Crypto Exchange", "blurb": "Crypto exchange complaints include frozen accounts and delayed withdrawals."},
  {"name": "Capital Systematic", "slug": "capitalsystematic", "url": "capitalsystematic.org", "type": "Investment Platform", "blurb": ".org systematic-capital branding with reports of deposit traps and payout denial."},
  {"name": "Servelius", "slug": "servelius", "url": "servelius.com", "type": "Investment / Trading Platform", "blurb": "Complaints cite opaque operators and funds that cannot be withdrawn."},
  {"name": "AI Trade 24", "slug": "aitrade24", "url": "aitrade24.com", "type": "AI Trading Platform", "blurb": "AI trading claims with reports of fabricated results and blocked withdrawals."},
  {"name": "The Toro Global", "slug": "thetoroglobal", "url": "thetoroglobal.com", "type": "Investment Platform", "blurb": "Global branding with complaints about high-pressure deposits and stalled cash-outs."},
  {"name": "Dusk Market Trade", "slug": "duskmarkettrade", "url": "duskmarkettrade.com", "type": "Trading Platform", "blurb": "Market-trade pitch with reports of withdrawal blocks and fee loops."},
  {"name": "Les Rouleaux", "slug": "lesrouleaux", "url": "lesrouleaux.com", "type": "Investment / Trading Platform", "blurb": "Users report deposit pressure and inability to access balances."},
  {"name": "Spreadex4", "slug": "spreadex4", "url": "spreadex4.com", "type": "Trading Platform", "blurb": "Spread/trading branding with clone-style naming risks and withdrawal complaints."},
  {"name": "GSI Markets", "slug": "gsimarkets", "url": "gsimarkets.com", "type": "Trading Platform", "blurb": "Markets branding with reports of blocked withdrawals and unverifiable regulation."},
  {"name": "Coin Birds", "slug": "coin-birds", "url": "coin-birds.com", "type": "Crypto Platform", "blurb": "Crypto pitch with complaints about locked wallets and missing payouts."},
  {"name": "Adbit", "slug": "adbit", "url": "adbit.pro", "type": "Crypto / Ad Platform", "blurb": ".pro domain with reports of deposit-only activity and opaque operators."},
  {"name": "Core Various", "slug": "corevarious", "url": "corevarious.com", "type": "Investment Platform", "blurb": "Users report aggressive solicitation and withdrawal obstruction."},
  {"name": "StockTwits", "slug": "stocktwits", "url": "stocktwits.com", "type": "Platform Review", "blurb": "This page compiles publicly reported complaints tied to this domain. StockTwits is also a known social investing brand — verify claims independently."},
  {"name": "Odecent", "slug": "odecent", "url": "odecent.com", "type": "Trading / Investment Platform", "blurb": "Complaints include deposit pressure, fake profits, and stalled payouts."},
  {"name": "Diamond FX", "slug": "diamondfx", "url": "diamondfx.com", "type": "Forex Trading Platform", "blurb": "FX branding with reports of blocked withdrawals and high-pressure account managers."},
  {"name": "Phillip Capital", "slug": "phillipcapital", "url": "phillipcapital.com", "type": "Broker Review", "blurb": "This page compiles publicly reported complaints. Phillip Capital also operates as a known brokerage brand — verify regulation independently."},
  {"name": "Vireo Finance", "slug": "vireofinance", "url": "vireofinance.net", "type": "Finance / Investment Platform", "blurb": "Finance branding with complaints about withdrawal denial and unverifiable licenses."},
  {"name": "Finanzhammer", "slug": "finanzhammer", "url": "finanzhammer.com", "type": "Investment Platform", "blurb": "Users report deposit traps and cash-outs blocked by unexpected fees."},
  {"name": "Crynvest", "slug": "crynvest", "url": "crynvest.com", "type": "Crypto Investment Platform", "blurb": "Crypto-invest pitch with reports of locked funds and silent support."},
  {"name": "Coinsmex", "slug": "coinsmex", "url": "coinsmex.net", "type": "Crypto Exchange", "blurb": "Exchange complaints include frozen accounts and delayed withdrawals."},
  {"name": "Evergrowth Finance", "slug": "evergrowthfinance", "url": "evergrowthfinance.com", "type": "Investment Platform", "blurb": "Growth branding with reports of fake returns and payout obstruction."},
  {"name": "Big Markets", "slug": "bigmarkets", "url": "bigmarkets.com", "type": "Trading Platform", "blurb": "Markets branding with complaints about blocked withdrawals and fee demands."},
  {"name": "Tradewell", "slug": "tradewell", "url": "tradewell.io", "type": "Trading Platform", "blurb": "Users report deposit pressure and dashboard balances that cannot be withdrawn."},
  {"name": "Emerald Holdings Ltd", "slug": "emeraldholdingsltd", "url": "emeraldholdingsltd.com", "type": "Investment Platform", "blurb": "Holdings branding with reports of stalled withdrawals and opaque ownership."},
  {"name": "Trendify FX", "slug": "trendifyfx", "url": "trendifyfx.com", "type": "Forex Trading Platform", "blurb": "FX trend branding with complaints about withdrawal blocks and fake profits."},
  {"name": "Voltizi FXT", "slug": "voltizifxt", "url": "voltizifxt.com", "type": "Forex Trading Platform", "blurb": "FXT branding with reports of deposit traps and unresponsive support."},
  {"name": "Perfect Forex Trading", "slug": "perfectforextrading", "url": "perfectforextrading.org", "type": "Forex Trading Platform", "blurb": ".org forex pitch with complaints about blocked cash-outs and unverifiable licenses."},
  {"name": "Imperium Firm", "slug": "imperiumfirm", "url": "imperiumfirm.com", "type": "Investment Platform", "blurb": "Firm branding with reports of high-pressure deposits and payout denial."},
  {"name": "Setwind Brokers", "slug": "setwindbrokers", "url": "setwindbrokers.com", "type": "Broker Platform", "blurb": "Broker branding with complaints about withdrawal obstruction and fee loops."},
  {"name": "Tani Minecraft", "slug": "taniminecraft", "url": "taniminecraft.pl", "type": "Platform Review", "blurb": "This page compiles publicly reported complaints tied to this domain. Verify independently before trusting any investment pitch."},
  {"name": "Cedrus Capital", "slug": "cedrus-capital", "url": "cedrus.capital", "type": "Investment Platform", "blurb": "Capital branding with reports of deposit pressure and stalled withdrawals."},
  {"name": "Clidd", "slug": "clidd", "url": "clidd.com", "type": "Trading / Investment Platform", "blurb": "Users report opaque operators and funds that cannot be withdrawn."},
  {"name": "Beograd Consulting", "slug": "beograd-consulting", "url": "beograd-consulting.com", "type": "Consulting / Investment Platform", "blurb": "Consulting branding with complaints about solicitation and blocked access to funds."},
  {"name": "Henley Spire", "slug": "henleyspire", "url": "henleyspire.com", "type": "Investment Platform", "blurb": "Spire branding with reports of fake returns and withdrawal denial."},
  {"name": "Elite Trade Ltd", "slug": "elitetradeltd", "url": "elitetradeltd.com", "type": "Trading Platform", "blurb": "Elite-trade branding with complaints about blocked withdrawals and fee demands."},
  {"name": "All Hour Care", "slug": "allhourcare", "url": "allhourcare.com", "type": "Platform Review", "blurb": "This page compiles publicly reported complaints tied to this domain. Verify independently."},
  {"name": "Crypstone Global Investments", "slug": "crypstoneglobalinvestments", "url": "crypstoneglobalinvestments.com", "type": "Crypto Investment Platform", "blurb": "Global crypto-invest pitch with reports of locked funds and payout obstruction."},
  {"name": "Star Pronto", "slug": "starpronto", "url": "starpronto.com", "alt_urls": ["starpronto.vip"], "type": "Trading / Investment Platform", "blurb": "Multiple domains reported (starpronto.com / starpronto.vip); complaints include deposit traps and blocked withdrawals."},
  {"name": "S9 Trader", "slug": "s9trader", "url": "s9trader.com", "type": "Trading Platform", "blurb": "Users report deposit pressure, fake profits, and stalled cash-outs."},
  {"name": "Alturex", "slug": "alturex", "url": "alturex.net", "type": "Trading / Crypto Platform", "blurb": "Complaints cite blocked withdrawals and unverifiable company details."},
  {"name": "Seller Deck Senna", "slug": "sellerdecksenna", "url": "sellerdecksenna.com", "type": "Trading / Investment Platform", "blurb": "Users report opaque ownership and inability to withdraw deposited funds."},
  {"name": "Ark Venture Funds", "slug": "arkventurefunds", "url": "arkventurefunds.com", "type": "Investment Fund Platform", "blurb": "Venture-fund branding with reports of deposit traps and payout denial."},
  {"name": "Next Leap", "slug": "nextleap", "url": "nextleap.vip", "type": "Investment Platform", "blurb": ".vip domain with complaints about high-pressure deposits and blocked cash-outs."},
  {"name": "GF Star Group", "slug": "gfstargroup", "url": "gfstargroup.com", "type": "Investment Platform", "blurb": "Group branding with reports of stalled withdrawals and unverifiable licenses."},
  {"name": "Troop Whale App", "slug": "troopwhaleapp", "url": "troopwhaleapp.com", "type": "Trading App", "blurb": "App-style platform with complaints about unexpected fees and locked balances."},
  {"name": "TLN Prime", "slug": "tlnprime", "url": "tlnprime.com", "type": "Trading Platform", "blurb": "Prime branding with reports of withdrawal blocks and account-manager pressure."},
  {"name": "BitBloomX", "slug": "bitbloomx", "url": "bitbloomx.com", "type": "Crypto Platform", "blurb": "Crypto branding with complaints about frozen funds and missing payouts."},
  {"name": "Icrypex", "slug": "icrypex", "url": "icrypex.com", "type": "Crypto Exchange", "blurb": "This page compiles publicly reported complaints about withdrawals and support. Verify independently."},
  {"name": "Kairox", "slug": "kairox", "url": "kairox.cc", "type": "Crypto / Trading Platform", "blurb": ".cc domain with reports of deposit traps and blocked withdrawals."},
  {"name": "Acccat", "slug": "acccat", "url": "acccat.com", "type": "Trading / Investment Platform", "blurb": "Users report opaque operators and funds that cannot be withdrawn."},
  {"name": "One Two Markets", "slug": "onetwomarkets", "url": "onetwomarkets.co.za", "type": "Trading Platform", "blurb": "ZA markets branding with complaints about stalled cash-outs and fee demands."},
  {"name": "Stonewall Capital", "slug": "stonewallcapital", "url": "stonewallcapital.co.za", "type": "Investment Platform", "blurb": "Capital branding with reports of deposit pressure and payout obstruction."},
  {"name": "Number One Capital Market", "slug": "n1cm", "url": "n1cm.com", "type": "Forex / CFD Broker", "blurb": "This page compiles publicly reported complaints about N1CM. Verify regulatory claims independently."},
  {"name": "Trillium Financial Broker", "slug": "trilliumfinancialbroker", "url": "trilliumfinancialbroker.com", "type": "Broker Platform", "blurb": "Broker branding with reports of blocked withdrawals and unverifiable credentials."},
  {"name": "Bullwaves Prime", "slug": "bullwaves-prime", "url": "prime.bullwaves.com", "type": "Trading Platform", "blurb": "Prime subdomain with complaints about deposit pressure and stalled cash-outs."},
  {"name": "Doo Prime", "slug": "dooprime", "url": "dooprime.com", "type": "Broker Platform", "blurb": "This page compiles publicly reported complaints about Doo Prime. Verify regulation independently."},
  {"name": "BXB Market", "slug": "bxbmarket", "url": "bxbmarket.com", "type": "Trading Platform", "blurb": "Market branding with reports of withdrawal blocks and high-pressure upselling."},
  {"name": "XTrend Speed", "slug": "xtrendspeed", "url": "xtrendspeed.com", "type": "Trading App / Platform", "blurb": "Trading-app branding with complaints about blocked withdrawals and opaque operators."},
  {"name": "Aurum Foundation", "slug": "aurum-foundation", "url": "aurum.foundation", "type": "Investment / Crypto Platform", "blurb": "Foundation branding with reports of deposit traps and unverifiable claims."},
  {"name": "KCEX", "slug": "kcex", "url": "kcex.com", "type": "Crypto Exchange", "blurb": "This page compiles publicly reported complaints about withdrawals and account restrictions. Verify independently."},
  {"name": "BG Wealth Sharing Ltd", "slug": "bgwealthsharingltd", "url": "bgwealthsharingltd.com", "type": "Investment Platform", "blurb": "Wealth-sharing pitch with reports of locked funds and payout denial."},
  {"name": "Goldmann Co Limited", "slug": "goldmanncolimited", "url": "goldmanncolimited.net", "type": "Investment Platform", "blurb": "Lookalike corporate naming with complaints about deposit traps and stalled withdrawals."},
  {"name": "Klydex Edge", "slug": "klydexedge", "url": "klydexedge.com", "type": "Trading Platform", "blurb": "Edge branding with reports of blocked cash-outs and fee loops."},
  {"name": "Aurensthe Livix", "slug": "aurensthelivix", "url": "aurensthelivix.com", "type": "Trading / Investment Platform", "blurb": "Users report opaque ownership and inability to withdraw deposited funds."},
  {"name": "AIE Polymer", "slug": "aiepolymer", "url": "aiepolymer.com", "type": "Investment / Tech Platform", "blurb": "Tech branding with complaints about solicitation and blocked access to funds."},
  {"name": "Klydex Elite", "slug": "klydexelite", "url": "klydexelite.com", "type": "Trading Platform", "blurb": "Related elite branding with reports of deposit pressure and withdrawal denial."},
]

REVIEW_CSS = """
    .review-layout{display:grid;grid-template-columns:2fr 1fr;gap:3.5rem;align-items:start}
    .rbody h2{font-family:'Source Serif 4',Georgia,serif;font-size:1.55rem;color:var(--text);margin:2.2rem 0 .9rem;font-weight:600}
    .rbody h3{font-size:1.02rem;color:var(--blue);margin:1.6rem 0 .6rem;font-weight:600}
    .rbody p{color:var(--text-2);margin-bottom:1rem;font-size:.95rem;line-height:1.75}
    .rbody ul{margin:1rem 0 1.4rem 1.4rem;color:var(--text-2);font-size:.92rem}
    .rbody ul li{margin-bottom:.45rem;line-height:1.65}
    .rbody a{color:var(--blue)}
    .complaint-badge{display:inline-flex;align-items:center;gap:.4rem;font-size:.75rem;font-weight:600;padding:.35rem .85rem;border-radius:4px;margin-bottom:1rem}
    .badge-red{background:rgba(185,28,28,.1);color:#b91c1c;border:1px solid rgba(185,28,28,.25)}
    .badge-yellow{background:rgba(180,83,9,.08);color:#b45309;border:1px solid rgba(180,83,9,.22)}
    .complaint-box{background:#fff;border:1px solid #e2e8f0;border-left:3px solid #b91c1c;border-radius:4px;padding:1.15rem 1.35rem;margin:0 0 .85rem;box-shadow:none}
    .complaint-box .cq{font-size:.7rem;color:var(--blue);font-weight:600;margin-bottom:.4rem;text-transform:uppercase;letter-spacing:.07em}
    .complaint-box p{margin:0;font-size:.88rem;font-style:italic;color:var(--text-2);line-height:1.55}
    .page-hero h1{overflow-wrap:anywhere;word-break:break-word;max-width:100%}
    .checklist{list-style:none!important;margin-left:0!important}
    .checklist li{padding:.35rem 0;display:flex;gap:.65rem}
    .checklist li::before{content:"✓";color:var(--blue);font-weight:700;flex-shrink:0}
    .sidebar-widget{background:var(--bg-3);border:1px solid var(--line);border-radius:6px;padding:1.5rem;margin-bottom:1.2rem}
    .sidebar-widget.sticky-form{position:sticky;top:92px}
    .sidebar-widget h3{font-family:'Source Serif 4',Georgia,serif;font-size:1rem;color:var(--text);margin-bottom:.85rem;padding-bottom:.6rem;border-bottom:1px solid var(--line);font-weight:600}
    .sidebar-widget .form-group{margin-bottom:.75rem}
    .sidebar-widget .form-group label{color:var(--text-2);margin-bottom:.35rem}
    .sidebar-widget .form-group input,
    .sidebar-widget .form-group select,
    .sidebar-widget .form-group textarea{
      width:100%;background:#fff;border:1px solid #e2e8f0;border-radius:4px;
      padding:.7rem .85rem;color:var(--ink);font-family:'DM Sans',sans-serif;font-size:.86rem;
      line-height:1.35;outline:none;appearance:none;-webkit-appearance:none;box-shadow:none;
      transition:border-color .15s,box-shadow .15s
    }
    .sidebar-widget .form-group select{
      padding-right:2.3rem;cursor:pointer;
      background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='%2364748b' d='M1.2 1.5L6 6.3 10.8 1.5 12 2.7 6 8.7 0 2.7z'/%3E%3C/svg%3E");
      background-repeat:no-repeat;background-position:right .85rem center;background-size:12px 8px;background-color:#fff
    }
    .sidebar-widget .form-group select option{background:#fff;color:var(--ink)}
    .sidebar-widget .form-group input:focus,
    .sidebar-widget .form-group select:focus,
    .sidebar-widget .form-group textarea:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(37,99,235,.12)}
    .sidebar-widget .form-group textarea{min-height:88px;resize:vertical}
    .sidebar-widget form .btn{border-radius:4px!important;width:100%;margin-top:.15rem}
    .slinks{list-style:none;margin:0;padding:0}
    .slinks li{padding:.45rem 0;border-bottom:1px solid rgba(15,23,42,.06)}
    .slinks a{color:var(--text-2);font-size:.86rem;text-decoration:none}
    .slinks a:hover{color:var(--blue)}
    @media(max-width:768px){.review-layout{grid-template-columns:1fr}.sidebar-widget.sticky-form{position:static}}
"""


def related_links(current_slug, n=4):
    others = [b for b in BROKERS if b["slug"] != current_slug]
    # deterministic-ish pick: neighbors by index
    idx = next(i for i, b in enumerate(BROKERS) if b["slug"] == current_slug)
    picks = []
    for off in range(1, len(BROKERS)):
        picks.append(others[(idx + off - 1) % len(others)])
        if len(picks) >= n:
            break
    return picks


def review_html(b):
    name = b["name"]
    slug = b["slug"]
    url = b.get("url") or "not publicly confirmed"
    alt = b.get("alt_urls") or []
    url_line = f"<code>{url}</code>"
    if alt:
        url_line += " (also reported: " + ", ".join(f"<code>{u}</code>" for u in alt) + ")"
    related = related_links(slug)
    related_html = "\n".join(
        f'      <li><a href="{r["slug"]}-review.html">Is {r["name"]} a Scam?</a></li>' for r in related
    )
    domain_label = url if b.get("url") else "unverified domain"
    desc = (
        f"Is {name} a scam? {name} review of complaints, withdrawal problems, and regulatory warnings "
        f"({domain_label}). {b['blurb']} Learn how to report {name} and verify if it is legit."
    )
    keywords = (
        f"is {name} a scam, {name} review, {name} scam, is {name} legit, "
        f"{name} complaints, {name} withdrawal problem, how to report {name}, {slug}-review"
    )
    schema_headline = f"Is {name} a Scam? {name} Review – Complaints & How to Report"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Is {name} a Scam? {name} Review – Complaints, Warnings & How to Report | {BRAND_FULL}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{DOMAIN}/reviews/{slug}-review.html">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article","headline":"{schema_headline}","description":"{b['blurb']}","author":{{"@type":"Organization","name":"{BRAND}"}},"publisher":{{"@type":"Organization","name":"{BRAND}"}}}}
  </script>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/comments.css">
  <style>{REVIEW_CSS}
  </style>
</head>
<body>
<div id="nav-placeholder"></div>
<div class="breadcrumb"><a href="../index.html">Home</a><span>›</span><a href="index.html">Broker Reviews</a><span>›</span> {name}</div>

<div class="page-hero">
  <div class="hero-badge">{b['type']} · Scam Check</div>
  <h1 data-company="{name}">Is {name} a Scam? {name} Review</h1>
  <p>Is {name} legit? {b['blurb']}</p>
</div>

<section>
<div class="review-layout">
<div class="rbody">

  <span class="complaint-badge badge-red">Multiple Fraud Reports</span>

  <p><strong style="color:var(--text)">Editorial note:</strong> This {name} review compiles publicly reported user complaints and available regulatory information. We recommend verifying all claims independently using the official regulatory links below. If you have been defrauded by this platform, report it immediately using the guidance at the bottom of this page.</p>

  <p><strong style="color:var(--text)">Reported website:</strong> {url_line}</p>

  <h2>Is {name} a Scam? What Users Are Reporting</h2>
  <p>People searching “is {name} a scam” or “is {name} legit” usually hit the same pattern: {name} presents itself as a legitimate trading or investment service — yet when withdrawal requests are submitted, accounts are delayed, locked, or hit with unexpected fees.</p>
  <p>A recurring pattern involves account managers who are highly responsive during the deposit phase but become difficult to reach once a user requests a withdrawal. Several complainants describe dashboard balances that appear profitable until a cash-out attempt is made.</p>
  <p>{name} does not appear with clear, independently verifiable registration in major FCA, SEC, ASIC, or CySEC public registers under commonly reported company details. Absence of verifiable regulation is a significant warning sign for any platform handling client funds.</p>

  <h2>{name} Complaints: Common Patterns</h2>

  <div class="complaint-box">
    <div class="cq">User Complaint Pattern #1 — Withdrawal Issues</div>
    <p>"When I tried to withdraw my balance, I was told I needed to pay a tax or clearance fee first. After paying, another fee appeared. Support stopped responding."</p>
  </div>

  <div class="complaint-box">
    <div class="cq">User Complaint Pattern #2 — Account Manager Pressure</div>
    <p>"My account manager kept contacting me to deposit more, saying my position was about to become very profitable. After I deposited, they became unreachable."</p>
  </div>

  <div class="complaint-box">
    <div class="cq">User Complaint Pattern #3 — Fake Platform Profits</div>
    <p>"The platform showed strong profits for weeks. When I tried to take out money I was told I owed compliance fees. The profits were never withdrawable."</p>
  </div>

  <h2>Is {name} Legit? How to Verify Regulatory Status</h2>
  <p>Before trusting any broker or trading platform with your funds, verify their regulatory status using these official databases:</p>
  <ul class="checklist">
    <li>FCA Register (UK): register.fca.org.uk — search the exact company name</li>
    <li>SEC EDGAR (US): sec.gov/cgi-bin/browse-edgar — check for registration</li>
    <li>FINRA BrokerCheck (US): brokercheck.finra.org</li>
    <li>ASIC Connect (Australia): connectonline.asic.gov.au</li>
    <li>CySEC (Cyprus/EU): cysec.gov.cy/en-GB/entities/</li>
    <li>CFTC (US commodity/forex): cftc.gov/check</li>
  </ul>
  <p>If you cannot find {name} in any regulatory register, treat this as a serious warning sign. Unregulated platforms have no reliable consumer-protection obligation to return client funds.</p>

  <div class="alert alert-amber">
    <h4>Clone Firm Warning</h4>
    <p>Some fraudulent platforms copy the name, registration number, or branding of legitimate regulated firms. Always verify the exact URL, phone number, and contact details against the official regulator's website — not information provided by the firm itself.</p>
  </div>

  <h2>How to Report {name}</h2>
  <p>If you have lost money to this platform, take these steps immediately:</p>
  <ul>
    <li><strong>Contact your bank</strong> within 24–48 hours — wire transfers may be recallable</li>
    <li><strong>Report to your national fraud authority:</strong> FTC at ReportFraud.ftc.gov (US) | Action Fraud / Report Fraud (UK) | Scamwatch at scamwatch.gov.au (AU)</li>
    <li><strong>File with your financial regulator:</strong> FCA (UK), SEC/CFTC (US), ASIC (AU)</li>
    <li><strong>Report the website</strong> to Google Safe Browsing and Microsoft/Bing</li>
    <li><strong>Document everything:</strong> screenshots, transaction IDs, all communications</li>
    <li><strong>Consider a private investigator</strong> — consultation is free — <a href="../pages/private-investigator.html">find one here</a></li>
  </ul>

  <h2>Frequently Asked Questions</h2>
  <h3>Is {name} a scam?</h3>
  <p>Based on publicly reported complaints — blocked withdrawals, deposit pressure, and weak or missing regulatory proof — {name} shows multiple red flags associated with fraudulent brokers. This does not replace an official regulator finding. Verify the firm yourself in FCA, SEC, ASIC, or CySEC registers and treat unverifiable licenses as a serious warning.</p>

  <h3>Is {name} legit?</h3>
  <p>A legit broker can be confirmed on an official regulator register with matching legal name, URL, and license number. If {name} cannot be verified that way, do not treat marketing claims or a polished website as proof of legitimacy.</p>

  <h3>Can I get my money back from {name}?</h3>
  <p>Recovery depends on how payment was made and how quickly you act. Bank transfers reported within 24–48 hours have the best chance of recall. Cryptocurrency is harder but may be traceable through blockchain forensics. A licensed investigator can assess your specific situation. <a href="../pages/contact.html">Submit your case for a free review.</a></p>

  <h3>Is there a class action or group claim against {name}?</h3>
  <p>We are aware of multiple victims reporting similar experiences with platforms matching this pattern. If you would like to be connected with others who may have been affected, <a href="../pages/contact.html">contact our case team</a>.</p>

  <h3>What should I do if {name} contacts me again?</h3>
  <p>Do not respond or send any more funds. Any contact after a withdrawal dispute — especially offering to "release" your funds for a fee — is almost certainly part of an escalating fraud. Document the contact and report it to your fraud authority.</p>

</div>

<div>
  <div class="sidebar-widget sticky-form">
    <h3>Lost Money to {name}?</h3>
    <p style="color:var(--text-2);font-size:.85rem;margin-bottom:1.1rem">Consultation is free — licensed investigators respond within 24 hours.</p>
    <form class="contact-form" data-formcarry action="https://formcarry.com/s/cxJd01H31MD" method="POST" accept-charset="UTF-8">
    <input type="hidden" name="_page" value="reviews_{slug}-review">
    <div class="form-group"><label>Your Email</label><input type="email" placeholder="your@email.com" name="email" required></div>
    <div class="form-group"><label>Amount Lost</label>
    <select name="loss_amount" required><option value="" disabled selected>Select range...</option><option value="Under $1,000">Under $1,000</option><option value="$1,000–$25,000">$1,000–$25,000</option><option value="$25,000–$100,000">$25,000–$100,000</option><option value="Over $100,000">Over $100,000</option></select></div>
    <div class="form-group"><label>What happened?</label><textarea name="description" placeholder="Brief description..." required></textarea></div>
    <button type="submit" class="btn btn-amber btn-block">Request Free Consultation</button>
    </form>
  </div>
  <div class="sidebar-widget">
    <h3>Related Reviews</h3>
    <ul class="slinks">
{related_html}
      <li><a href="index.html">All Reviews →</a></li>
    </ul>
  </div>
  <div class="sidebar-widget">
    <h3>Report Links</h3>
    <ul class="slinks">
      <li><a href="../pages/report-a-scam.html">Report a Scam</a></li>
      <li><a href="../pages/action-fraud.html">Action Fraud (UK)</a></li>
      <li><a href="../pages/federal-trade-commission.html">FTC (US)</a></li>
      <li><a href="../pages/private-investigator.html">Find a PI</a></li>
    </ul>
  </div>
</div>
</div>
</section>

<section class="cta-section">
  <h2>Were You Defrauded by {name}?</h2>
  <p>Our licensed investigators specialize in broker fraud. Get a free, confidential consultation today.</p>
  <a href="../pages/contact.html" class="btn btn-amber">Get Free Consultation</a>
  <a href="../pages/report-a-scam.html" class="btn btn-outline" style="margin-left:1rem">Report Now</a>
</section>

<div id="footer-placeholder"></div>
<script src="../js/config.js"></script>
<script src="../js/layout.js"></script>
<script src="../js/comments.js"></script>
<script src="../js/comments-inject.js"></script>
</body>
</html>
"""


def reviews_index_html():
    cards = []
    for b in BROKERS:
        url_note = b["url"] if b.get("url") else "Domain unverified"
        cards.append(f"""
    <div class="review-card">
      <span class="complaint-badge badge-red">Scam Check</span>
      <h3><a href="{b['slug']}-review.html">Is {b['name']} a Scam? Review</a></h3>
      <p>Is {b['name']} legit? {b['blurb']}</p>
      <div class="review-meta"><span>{b['type']}</span><span>{url_note}</span></div>
      <a href="{b['slug']}-review.html" class="read-link">Read Complaints & How to Report →</a>
    </div>""")
    cards_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Broker Reviews: Is This Broker a Scam? Complaints & Warnings | {BRAND_FULL}</title>
  <meta name="description" content="Broker reviews and scam checks. Is this broker legit? Browse complaint reports, withdrawal warnings, and how to report fraudulent trading platforms.">
  <meta name="keywords" content="broker review, broker scam, is this broker a scam, broker complaints, trading platform review, how to report broker scam">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{DOMAIN}/reviews/">
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .review-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.4rem;margin-top:2.5rem}}
    .review-card{{background:var(--bg-3);border:1px solid var(--line);border-radius:6px;padding:1.6rem;transition:border-color .2s,transform .2s}}
    .review-card:hover{{transform:translateY(-2px);border-color:var(--blue)}}
    .review-card h3{{font-family:'Source Serif 4',Georgia,serif;color:var(--text);font-size:1.05rem;margin-bottom:.45rem;font-weight:600}}
    .review-card h3 a{{color:inherit;text-decoration:none}}
    .review-card h3 a:hover{{color:var(--blue)}}
    .review-card p{{color:var(--text-2);font-size:.88rem;line-height:1.55;margin-bottom:.9rem}}
    .complaint-badge{{display:inline-flex;align-items:center;gap:.35rem;font-size:.72rem;font-weight:600;padding:.28rem .7rem;border-radius:4px;margin-bottom:.7rem}}
    .badge-red{{background:rgba(185,28,28,.1);color:#b91c1c;border:1px solid rgba(185,28,28,.25)}}
    .review-meta{{font-size:.75rem;color:var(--text-2);display:flex;gap:.9rem;flex-wrap:wrap}}
    .read-link{{color:var(--blue);font-size:.84rem;font-weight:600;text-decoration:none;display:inline-block;margin-top:.7rem}}
    .warning-banner{{background:rgba(37,99,235,.06);border:1px solid rgba(37,99,235,.18);border-radius:6px;padding:1.3rem 1.6rem;margin-bottom:2.2rem}}
    .warning-banner p{{margin:0;color:var(--text-2);font-size:.9rem}}
  </style>
</head>
<body>
<div id="nav-placeholder"></div>
<div class="breadcrumb"><a href="../index.html">Home</a><span>›</span> Broker Reviews</div>

<div class="page-hero">
  <div class="hero-badge">Scam Checks · Complaint Database</div>
  <h1>Broker Reviews: Is This Broker a Scam?</h1>
  <p>Research before you invest. Each review covers complaints, withdrawal problems, regulation checks, and how to report the platform.</p>
</div>

<section>
  <div class="warning-banner">
    <p><strong style="color:var(--text)">Editorial Policy:</strong> Our reviews compile publicly available user complaints, regulatory alerts, and warning signals. We direct readers to official regulatory databases to verify claims independently. If you have been defrauded by any platform listed here, <a href="../pages/report-a-scam.html" style="color:var(--blue)">report it to the relevant authority</a> and <a href="../pages/contact.html" style="color:var(--blue)">contact our investigation team</a>.</p>
  </div>

  <div class="sec-tag">Platforms With Active Complaints</div>
  <h2 class="sec-title">Broker Complaint Reviews</h2>

  <div class="review-grid">
{cards_html}
  </div>
</section>

<section class="cta-section">
  <h2>Is Your Broker Not Listed?</h2>
  <p>Submit a complaint about any platform and our team will investigate and publish findings to help other potential victims.</p>
  <a href="../pages/contact.html" class="btn btn-amber">Submit a Broker Complaint</a>
</section>

<div id="footer-placeholder"></div>
<script src="../js/config.js"></script>
<script src="../js/layout.js"></script>
</body>
</html>
"""


def update_css():
    css_path = ROOT / "css" / "style.css"
    css = css_path.read_text(encoding="utf-8")
    # Replace font import + :root block start through first closing }
    new_header = """@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════
   GLOBUSNET DESIGN SYSTEM
   Aesthetic: Corporate blue, minimal
   Fonts: Source Serif 4 + DM Sans + IBM Plex Mono
   ═══════════════════════════════════════════ */

:root {
  --ink:        #0f172a;
  --ink-mid:    #1e293b;
  --ink-light:  #334155;
  --ink-glass:  rgba(15, 23, 42, 0.88);
  --amber:      #2563eb;          /* primary corporate blue (legacy token) */
  --amber-2:    #3b82f6;
  --amber-dim:  rgba(37, 99, 235, 0.10);
  --amber-glow: rgba(37, 99, 235, 0.06);
  --blue:       #2563eb;
  --blue-2:     #3b82f6;
  --blue-dim:   rgba(37, 99, 235, 0.10);
  --fog:        #e2e8f0;
  --fog-mid:    #64748b;
  --fog-deep:   #475569;
  --white:      #f8fafc;
  --red:        #b91c1c;
  --red-dim:    rgba(185,28,28,0.10);
  --green:      #15803d;
  --border:     rgba(37, 99, 235, 0.14);
  --border-hi:  rgba(37, 99, 235, 0.32);
  --ease:       cubic-bezier(0.16, 1, 0.3, 1);
  /* page aliases used by review templates */
  --text:       #0f172a;
  --text-2:     #475569;
  --bg-3:       #ffffff;
  --bg-4:       #f1f5f9;
  --line:       #e2e8f0;
}
"""
    css = re.sub(
        r"^@import url\([^)]+\);\s*/\* ═+.*?^:root \{.*?\n\}\n",
        new_header + "\n",
        css,
        count=1,
        flags=re.S | re.M,
    )
    # Body: light corporate background
    css = css.replace(
        """body {
  font-family: 'Syne', sans-serif;
  background: var(--ink);
  color: var(--white);
  line-height: 1.7;
  overflow-x: hidden;
}""",
        """body {
  font-family: 'DM Sans', sans-serif;
  background: #f8fafc;
  color: var(--ink);
  line-height: 1.7;
  overflow-x: hidden;
}""",
    )
    css = css.replace("::selection { background: var(--amber); color: var(--ink); }",
                      "::selection { background: var(--blue); color: #fff; }")
    # Soften / remove heavy grain
    css = re.sub(
        r"/\* Noise grain \*/.*?z-index: 9998;\n\}",
        "/* Grain disabled for minimal corporate look */\nbody::after { display: none; }",
        css,
        count=1,
        flags=re.S,
    )
    # Nav scrolled: light
    css = css.replace(
        """nav.scrolled {
  background: rgba(7, 16, 31, 0.94);
  backdrop-filter: blur(20px);
  border-color: var(--border);
}""",
        """nav.scrolled {
  background: rgba(248, 250, 252, 0.94);
  backdrop-filter: blur(16px);
  border-color: var(--line);
}""",
    )
    css = css.replace(
        """.nav-logo {
  font-family: 'Syne', sans-serif;
  font-weight: 800; font-size: 1.2rem; letter-spacing: -0.3px;
  color: var(--white); text-decoration: none;
}
.nav-logo span { color: var(--amber); }""",
        """.nav-logo {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700; font-size: 1.15rem; letter-spacing: -0.3px;
  color: var(--ink); text-decoration: none;
}
.nav-logo span { color: var(--blue); }""",
    )
    css = css.replace(
        """.nav-cta {
  background: var(--amber) !important; color: var(--ink) !important;
  font-weight: 700 !important; border-radius: 7px !important;
  padding: 0.5rem 1rem !important; font-size: 0.78rem !important;
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s !important;
  white-space: nowrap;
}
.nav-cta:hover {
  background: var(--amber-2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(212,168,67,0.3) !important;
}""",
        """.nav-cta {
  background: var(--blue) !important; color: #fff !important;
  font-weight: 600 !important; border-radius: 4px !important;
  padding: 0.5rem 1rem !important; font-size: 0.78rem !important;
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s !important;
  white-space: nowrap;
}
.nav-cta:hover {
  background: var(--blue-2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 18px rgba(37,99,235,0.25) !important;
}""",
    )
    # Font family swaps
    css = css.replace("'Syne', sans-serif", "'DM Sans', sans-serif")
    css = css.replace("'Cormorant Garamond', serif", "'Source Serif 4', Georgia, serif")
    css = css.replace("'JetBrains Mono', monospace", "'IBM Plex Mono', monospace")
    css = css.replace("'Playfair Display', serif", "'Source Serif 4', Georgia, serif")
    # Mobile overlay light-ish but readable - keep dark navy for contrast
    css = css.replace("background: rgba(7,16,31,0.98)", "background: rgba(15,23,42,0.97)")
    css = css.replace(
        "box-shadow: 0 6px 20px rgba(212,168,67,0.3)",
        "box-shadow: 0 6px 18px rgba(37,99,235,0.25)",
    )
    # Page hero / section text for light theme
    # Add utility overrides at end
    css += """

/* ─── Light corporate overrides ─── */
.page-hero h1, .sec-title, .cta-section h2, .article-body h2, footer .nav-logo { color: var(--ink); }
.page-hero p, .cta-section p { color: var(--text-2); }
.page-hero { background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 100%); border-bottom: 1px solid var(--line); }
.hero-badge, .sec-tag {
  color: var(--blue) !important;
  background: var(--blue-dim) !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
}
.btn-amber, .btn-primary {
  background: var(--blue) !important;
  color: #fff !important;
  border-radius: 4px !important;
  box-shadow: none !important;
}
.btn-amber:hover, .btn-primary:hover { background: var(--blue-2) !important; }
.btn-outline { border-color: var(--blue) !important; color: var(--blue) !important; border-radius: 4px !important; }
.cta-section { background: #eff6ff; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
footer { background: var(--ink); color: var(--fog); }
footer .nav-logo { color: #fff !important; }
footer a { color: #94a3b8; }
.breadcrumb { color: var(--fog-mid); }
.breadcrumb a { color: var(--blue); }
.alert-amber { background: rgba(37,99,235,.06); border: 1px solid rgba(37,99,235,.2); }
.form-group label { color: var(--text-2); }
.form-group input, .form-group select, .form-group textarea {
  background: #fff; border: 1px solid var(--line); color: var(--ink); border-radius: 4px;
}
.mobile-overlay .mobile-nav a { color: #cbd5e1; }
.mobile-cta { background: var(--blue) !important; color: #fff !important; border-radius: 4px !important; }
"""
    css_path.write_text(css, encoding="utf-8")
    print("Updated css/style.css")


def update_layout():
    layout = ROOT / "js" / "layout.js"
    text = layout.read_text(encoding="utf-8")
    text = text.replace("ACT HERE — act-here.org", "GLOBUSNET — globusnet.org")
    text = text.replace('Act<span>Here</span>', 'Globus<span>Net</span>')
    text = text.replace("Act-Here", BRAND)
    text = text.replace("Act Here", BRAND)
    text = text.replace("act-here.org", "globusnet.org")
    # Soften CTA copy slightly
    text = text.replace("Get Help — $1,000+ Losses", "Get Help")
    text = text.replace("Get Help — $1,000+ Losses", "Get Help")
    layout.write_text(text, encoding="utf-8")
    print("Updated js/layout.js")

    config = ROOT / "js" / "config.js"
    c = config.read_text(encoding="utf-8")
    c = c.replace("ACT-HERE.COM", "GLOBUSNET.ORG")
    c = c.replace("ACT_HERE_CONFIG", "GLOBUSNET_CONFIG")
    c = c.replace("act-here.org", "globusnet.org")
    c = c.replace("hello@act-here.org", "hello@globusnet.org")
    # Fix runtime references if any
    c = c.replace("ACT_HERE_CONFIG", "GLOBUSNET_CONFIG")
    config.write_text(c, encoding="utf-8")
    # layout may still reference ACT_HERE_CONFIG via config - config self-refs updated
    # Check layout for ACT_HERE
    print("Updated js/config.js")


def brand_replace_all():
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".html", ".xml", ".js", ".txt", ".css"}:
            continue
        if path.name.startswith("_generate"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = text
        text = text.replace("https://act-here.org", DOMAIN)
        text = text.replace("act-here.org", "globusnet.org")
        text = text.replace("Act-Here.org", BRAND_FULL)
        text = text.replace("Act-Here", BRAND)
        text = text.replace("Act Here", BRAND)
        text = text.replace("ACT HERE", "GLOBUSNET")
        text = text.replace("hello@act-here.org", "hello@globusnet.org")
        # Fix broken script path on old root reviews index if any
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(f"Branded: {path.relative_to(ROOT)}")


def write_sitemap():
    urls = [
        ("/", "1.0"),
        ("/reviews/", "0.9"),
        ("/pages/report-a-scam.html", "0.85"),
        ("/pages/how-to-report-a-scam.html", "0.85"),
        ("/pages/contact.html", "0.8"),
        ("/pages/about.html", "0.7"),
        ("/pages/crypto-scams.html", "0.8"),
        ("/pages/investment-fraud.html", "0.8"),
        ("/pages/private-investigator.html", "0.8"),
        ("/pages/fraud-authorities.html", "0.75"),
        ("/pages/faq.html", "0.7"),
    ]
    for b in BROKERS:
        urls.append((f"/reviews/{b['slug']}-review.html", "0.8"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri in urls:
        lines.append(
            f"  <url><loc>{DOMAIN}{loc}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>{pri}</priority></url>"
        )
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote sitemap.xml")


def write_home():
    # Simple corporate homepage pointing to reviews
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{BRAND} — Fraud Reporting & Broker Complaint Reviews</title>
  <meta name="description" content="GlobusNet helps scam victims report fraud and research broker complaints. Crypto forensics guidance, reporting directories, and investigator referrals.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{DOMAIN}/">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="nav-placeholder"></div>

<section class="page-hero" style="padding-top:8rem;padding-bottom:4rem;">
  <div class="hero-badge">Fraud Reporting · Broker Reviews</div>
  <h1>Research Brokers.<br>Report Fraud. Act with Clarity.</h1>
  <p style="max-width:560px;margin-top:1rem;">GlobusNet compiles broker complaint reviews and step-by-step fraud reporting guidance so victims know who to contact — and what evidence regulators need.</p>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:2rem;">
    <a href="reviews/index.html" class="btn btn-amber">Browse Broker Reviews</a>
    <a href="pages/report-a-scam.html" class="btn btn-outline">Report a Scam</a>
  </div>
</section>

<section>
  <div class="sec-tag">What We Do</div>
  <h2 class="sec-title">Clear guidance when fraud hits</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.2rem;margin-top:2rem;">
    <div style="background:#fff;border:1px solid var(--line);border-radius:6px;padding:1.5rem;">
      <h3 style="font-family:'Source Serif 4',Georgia,serif;margin-bottom:.5rem;">Broker Reviews</h3>
      <p style="color:var(--text-2);font-size:.9rem;">Complaint patterns, clone-firm warnings, and how to verify regulation before you invest.</p>
      <a href="reviews/index.html" style="color:var(--blue);font-weight:600;font-size:.85rem;">View reviews →</a>
    </div>
    <div style="background:#fff;border:1px solid var(--line);border-radius:6px;padding:1.5rem;">
      <h3 style="font-family:'Source Serif 4',Georgia,serif;margin-bottom:.5rem;">Report Fraud</h3>
      <p style="color:var(--text-2);font-size:.9rem;">Step-by-step paths to FTC, Action Fraud, and 50+ national authorities.</p>
      <a href="pages/report-a-scam.html" style="color:var(--blue);font-weight:600;font-size:.85rem;">Start a report →</a>
    </div>
    <div style="background:#fff;border:1px solid var(--line);border-radius:6px;padding:1.5rem;">
      <h3 style="font-family:'Source Serif 4',Georgia,serif;margin-bottom:.5rem;">Investigator Help</h3>
      <p style="color:var(--text-2);font-size:.9rem;">Connect with licensed investigators. Consultation is free.</p>
      <a href="pages/contact.html" style="color:var(--blue);font-weight:600;font-size:.85rem;">Get help →</a>
    </div>
  </div>
</section>

<section class="cta-section">
  <h2>Lost money to an online broker?</h2>
  <p>Document everything, report quickly, and request a free consultation.</p>
  <a href="pages/contact.html" class="btn btn-amber">Free Consultation</a>
</section>

<div id="footer-placeholder"></div>
<script src="js/config.js"></script>
<script src="js/layout.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("Wrote index.html homepage")


def main():
    reviews_dir = ROOT / "reviews"
    reviews_dir.mkdir(exist_ok=True)

    update_css()
    update_layout()

    for b in BROKERS:
        path = reviews_dir / f"{b['slug']}-review.html"
        path.write_text(review_html(b), encoding="utf-8")
    print(f"Wrote {len(BROKERS)} review pages")

    (reviews_dir / "index.html").write_text(reviews_index_html(), encoding="utf-8")
    print("Wrote reviews/index.html")

    write_home()
    write_sitemap()
    brand_replace_all()
    print("Done.")


if __name__ == "__main__":
    main()
